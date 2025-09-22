#!/usr/bin/env python3

from argparse import ArgumentParser
from typing import Dict, Set, List
import time
import re
import logging

from read_sdoc import extract_requirements_from_file, Requirement

log = logging.getLogger(__name__)

WHITELIST_ORPHANS = [
    r"^HLR-.*",
]

WHITELIST_LEAFS = [
    r"^SRS-.*",
]

BLACKLIST_DIRECT_RELATIONS = [
    # SRS should not directly relate to HLR.
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

    for orphan_uid in orphan_uids(requirements):
        if not is_whitelisted(orphan_uid, WHITELIST_ORPHANS):
            error(f"Requirement '{orphan_uid}' has no parents and is considered an orphan.")

    for leaf in leaf_nodes(requirements):
        if not is_whitelisted(leaf, WHITELIST_LEAFS):
            error(f"Requirement '{leaf}' is a leaf node (no children).")

    for req in requirements.values():
        for parent_uid in req.parents:
            parent_req = requirements.get(parent_uid)
            if parent_req is None:
                continue
            for (child_pattern, parent_pattern) in BLACKLIST_DIRECT_RELATIONS:
                if re.fullmatch(child_pattern, req.uid) and re.fullmatch(parent_pattern, parent_uid):
                    error(f"Requirement '{req.uid}' should not directly relate to '{parent_uid}'.")

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

if __name__ == "__main__":
    exit(main())