from strictdoc.backend.sdoc.reader import SDReader
from strictdoc.backend.sdoc.models.document import SDocDocument
from strictdoc.backend.sdoc.models.node import SDocNodeField
from strictdoc.backend.sdoc.models.node import SDocElementIF, SDocNodeIF
from strictdoc.backend.sdoc.models.reference import ParentReqReference, ChildReqReference

import os

from typing import List, Set, Dict, Generator

class Requirement:
    uid: str
    parents: Set[str]
    children: Set[str]
    component: str | None = None

    def __init__(self, uid: str):
        self.uid = uid
        self.parents = set()
        self.children = set()

def extract_requirements_from_file(sdoc_path: str) -> Dict[str, Requirement]:
    doc: SDocDocument = SDReader().read(
        open(sdoc_path).read(),
        os.path.basename(sdoc_path),
    )
    requirements: Dict[str, Requirement] = {}
    for req in requirements_from_node(doc.section_contents):
        requirements[req.uid] = req
    # Populate children sets
    for req in requirements.values():
        for parent_uid in req.parents:
            parent_req = requirements.get(parent_uid)
            if parent_req:
                parent_req.children.add(req.uid)
            else:
                raise Exception(f"Parent UID '{parent_uid}' referenced by '{req.uid}' not found in requirements.")
    return requirements

def requirements_from_node(node: SDocElementIF | List[SDocElementIF]) -> Generator[Requirement, None, None]:
    if isinstance(node, list):
        for n in node:
            yield from requirements_from_node(n)
        return
    if not isinstance(node, SDocNodeIF):
        return
    node_type = node.node_type

    if node_type == "REQUIREMENT":
        fields: List[SDocNodeField] = getattr(node, "fields", [])
        uid: str | None = None
        component: str | None = None

        for field in fields:
            if field.field_name == "UID":
                uid = field.get_text_value()
            elif field.field_name == "COMPONENT":
                component = field.get_text_value()

        if uid is None:
            raise Exception("Requirement node without UID field.")

        requirement = Requirement(uid)
        requirement.component = component

        # get relations
        if hasattr(node, "relations"):
            relations = getattr(node, "relations", [])
            for rel in relations:
                if isinstance(rel, ParentReqReference):
                    requirement.parents.add(rel.ref_uid)
        yield requirement
    for c in node.section_contents:
        yield from requirements_from_node(c)
