#!/usr/bin/env python3

from argparse import ArgumentParser
from typing import Dict, Set, List, NewType, Tuple, Optional
import re
import logging

from read_sdoc import extract_requirements_from_file, Requirement

Range = NewType('Range', Tuple[Optional[int], Optional[int]])

log = logging.getLogger(__name__)

WHITELIST_ORPHANS = [
    r"^HLR-.*",
]

WHITELIST_LEAFS = [
    r"^SRS-.*",
]

# Complete specification of allowed direct parent relationships.
DIRECT_PARENT_RULES = [
    (r"^HLR-.*", [
        # HLR can only have other HLRs as parents.
        (r"^HLR-.*", Range((0, None))),
    ]),
    (r"^LLR-.*", [
        # LLR shall have at least one LLRs or HLRs as parent.
        (r"^(LLR|HLR)-.*", Range((1, None))),
    ]),
    (r"^SRS-.*", [
        # At least one LLR is required as parent of an SRS.
        (r"^LLR-.*", Range((1, None))),
        # SRS can also be a direct parent of SRS.
        (r"^SRS-.*", Range((0, None))),
    ]),
]

# Required child relationships, this is complementary to DIRECT_PARENT_RULES
REQUIRED_CHILDREN = [
    # LLR shall have at least one SRS child.
    (r"^LLR-.*", r"^SRS-.*"),
]

REQUIRED_PARENT_PATHS = [
    # SRS must have at least one HLR in its ancestry.
    (r"^SRS-.*", r"^HLR-.*"),
]

def main() -> int:
    parser = ArgumentParser(
        description="Check requirements in a StrictDoc SDoc file."
    )
    parser.add_argument(
        "sdoc_path",
        type=str,
        help="Path to the SDoc file to check.",
    )
    args = parser.parse_args()

    sdoc_path = args.sdoc_path
    requirements: Dict[str, Requirement] = extract_requirements_from_file(sdoc_path)

    has_errors = False
    def error(msg: str):
        nonlocal has_errors
        has_errors = True
        log.error(msg)

    # Check orphan nodes
    for orphan_uid in orphan_uids(requirements):
        if not is_whitelisted(orphan_uid, WHITELIST_ORPHANS):
            error(f"Requirement '{orphan_uid}' has no parents and is considered an orphan.")

    # Check leaf nodes
    for leaf in leaf_nodes(requirements):
        if not is_whitelisted(leaf, WHITELIST_LEAFS):
            error(f"Requirement '{leaf}' is a leaf node (no children).")

    # Check direct parent rules
    for req in requirements.values():
        # Find the rule that applies to this requirement
        matching_rule = None
        for child_pattern, parent_rules in DIRECT_PARENT_RULES:
            if re.fullmatch(child_pattern, req.uid):
                matching_rule = (child_pattern, parent_rules)
                break

        if matching_rule is None:
            error(f"No parent rule found for requirement '{req.uid}'.")
            continue

        parent_rules = matching_rule[1]

        used_parents: Set[str] = set()
        for parent_rule in parent_rules:
            pattern, rng = parent_rule
            selected_parents = [p for p in req.parents if re.fullmatch(pattern, p)]
            used_parents.update(selected_parents)
            if not is_in_range(len(selected_parents), rng):
                error(f"Requirement '{req.uid}' has {len(selected_parents)} parents matching '{pattern}', expected {display_rule(parent_rule)}.")
        unused_parents = set(req.parents) - used_parents
        if unused_parents:
            e = f"Requirement '{req.uid}' has parents {unused_parents} that do not match any parent rule:\n"
            for parent_rule in parent_rules:
                e += f"  - {req.uid} shall have {display_rule(parent_rule)}\n"
            error(e)

    # Check required children
    for req in requirements.values():
        for parent_pattern, child_pattern in REQUIRED_CHILDREN:
            if re.fullmatch(parent_pattern, req.uid):
                if not has_child_matching(req.uid, child_pattern, requirements):
                    error(f"Requirement '{req.uid}' must have at least one child matching '{child_pattern}'.")

    # Check required parent paths (ancestry requirements)
    for req in requirements.values():
        for child_pattern, ancestor_pattern in REQUIRED_PARENT_PATHS:
            if re.fullmatch(child_pattern, req.uid):
                if not has_ancestor_matching(req.uid, ancestor_pattern, requirements):
                    error(f"Requirement '{req.uid}' must have at least one ancestor matching '{ancestor_pattern}' in its parent chain.")

    # Check for cycles in the requirement graph
    cycles = detect_cycles(requirements)
    for cycle in cycles:
        cycle_str = " -> ".join(cycle + [cycle[0]])
        error(f"Cycle detected in requirements: {cycle_str}")

    return 1 if has_errors else 0

def is_whitelisted(uid: str, patterns: List[str]) -> bool:
    """Return True if uid matches any regex in patterns."""
    for pat in patterns:
        if re.fullmatch(pat, uid):
            return True
    return False

def orphan_uids(requirements: Dict[str, Requirement]) -> Set[str]:
    orphan_uids = set()
    for req in requirements.values():
        if not req.parents:
            orphan_uids.add(req.uid)
    return orphan_uids

def leaf_nodes(requirements: Dict[str, Requirement]) -> Set[str]:
    all_uids = set(requirements.keys())
    non_leaf_uids = set()
    for req in requirements.values():
        for parent_uid in req.parents:
            non_leaf_uids.add(parent_uid)
    return all_uids - non_leaf_uids

def detect_cycles(requirements: Dict[str, Requirement]) -> List[List[str]]:
    """Detect cycles in the requirements dependency graph using DFS."""
    WHITE, GRAY, BLACK = 0, 1, 2
    colors = {uid: WHITE for uid in requirements.keys()}
    cycles = []
    
    def dfs(uid: str, path: List[str]) -> None:
        if uid not in requirements:
            return
        
        if colors[uid] == GRAY:
            # Found a cycle - extract the cycle from the path
            cycle_start = path.index(uid)
            cycle = path[cycle_start:]
            cycles.append(cycle)
            return

        if colors[uid] == BLACK:
            return

        colors[uid] = GRAY
        path.append(uid)
        
        # Follow parent relationships (child -> parent edges)
        req = requirements[uid]
        for parent_uid in req.parents:
            dfs(parent_uid, path)

        path.pop()
        colors[uid] = BLACK

    # Start DFS from each unvisited node
    for uid in requirements.keys():
        if colors[uid] == WHITE:
            dfs(uid, [])

    return cycles

def has_ancestor_matching(uid: str, pattern: str, requirements: Dict[str, Requirement]) -> bool:
    """Check if a requirement has any ancestor (direct or indirect parent) matching the given pattern."""
    visited = set()
    
    def dfs_ancestors(current_uid: str) -> bool:
        if current_uid in visited:
            return False  # Avoid infinite loops in case of cycles
        visited.add(current_uid)

        req = requirements.get(current_uid)
        if req is None:
            return False

        # Check all direct parents
        for parent_uid in req.parents:
            if re.fullmatch(pattern, parent_uid):
                return True
            # Recursively check ancestors of this parent
            if dfs_ancestors(parent_uid):
                return True

        return False

    return dfs_ancestors(uid)

def has_child_matching(uid: str, pattern: str, requirements: Dict[str, Requirement]) -> bool:
    """Check if a requirement has any child (requirement that lists it as parent) matching the given pattern."""
    req = requirements.get(uid)
    if req is None:
        return False

    for child_uid in req.children:
        if re.fullmatch(pattern, child_uid):
            return True
    return False

def valid_range(rng: Range):
    min_count, max_count = rng
    if min_count is not None and min_count < 0:
        return False
    if max_count is not None and max_count < 0:
        return False
    if min_count is not None and max_count is not None and min_count > max_count:
        return False
    return True

def is_in_range(count: int, rng: Range) -> bool:
    assert valid_range(rng)
    min_count, max_count = rng
    if min_count is not None and count < min_count:
        return False
    if max_count is not None and count > max_count:
        return False
    return True

def display_rule(rule: Tuple[str, Range]):
    pattern, rng = rule
    (min_count, max_count) = rng
    assert valid_range(rng)
    if min_count is None and max_count is None:
        return f"any number of parents matching '{pattern}'"
    if min_count is None and max_count is not None:
        return f"at most {max_count} parents matching '{pattern}'"
    if max_count is None and min_count is not None:
        return f"at least {min_count} parents matching '{pattern}'"
    if min_count is not None and max_count is not None:
        if min_count == max_count:
            return f"exactly {min_count} parents matching '{pattern}'"
        return f"between {min_count} and {max_count} parents matching '{pattern}'"
    assert False, "Unreachable"

if __name__ == "__main__":
    exit(main())