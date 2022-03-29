"""This module contains the StallVisitor class"""


import libcst


class StallVisitor(libcst.VisitorMetadataProvider):
    """This class is used to iterate over the LibCST tree to find stall statements"""

    METADATA_DEPENDENCIES = (libcst.metadata.WhitespaceInclusivePositionProvider,)

    def __init__(self, module, reference):
        self._module = module
        self._reference = reference
        self._score = 0
        self._stall_dict = {}

    def visit_For_body(self, node) -> None:
        pos = self.get_metadata(
            libcst.metadata.WhitespaceInclusivePositionProvider, node
        ).start
        lines = self._module.code_for_node(node).splitlines()
        for index, line in enumerate(lines):
            if any(stall in line for stall in self._reference["sr_statements"]):
                if (pos.line + index) not in self._stall_dict:
                    self._score += 1
                    pos = self.get_metadata(
                        libcst.metadata.WhitespaceInclusivePositionProvider, node
                    ).start
                    actual_line = int(str(pos.line)) + index
                    if line.strip()[0:3] != '"""' and line.strip()[0] != "#":
                        self._stall_dict[actual_line] = line.strip()

    def visit_While_body(self, node) -> None:
        pos = self.get_metadata(
            libcst.metadata.WhitespaceInclusivePositionProvider, node
        ).start
        lines = self._module.code_for_node(node).splitlines()
        for index, line in enumerate(lines):
            if any(stall in line for stall in self._reference["sr_statements"]):
                if (pos.line + index) not in self._stall_dict:
                    self._score += 1
                    actual_line = pos.line + index
                    if line.strip()[0:3] != '"""' and line.strip()[0] != "#":
                        self._stall_dict[actual_line] = line.strip()

    def get_score(self):
        return self._score

    def get_stall_dict(self):
        return self._stall_dict
