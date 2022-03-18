"""This module contains the SRCalculator class"""

import libcst
import ast
import json
import os


class SRCalculator:
    """SRCalculator is responsible for calculation the SR of
    loop statements.
    """

    def __init__(self, filename):
        self._filename = filename
        self._reference_file = "stall_statements.json"
        self._sr_access = "sr_statements"
        self._sr_detections = (self._filename, [])

    def set_filename(self, filename):
        """Set the filename of that is currently being analyzed and
        remove any previous stall statements previously identified."""
        if filename is None:
            raise TypeError
        self._filename = filename
        self._sr_detections = (self._filename, [])

    def calculate_sr(self, nodes, libcst_module):
        """Calculate the Stall Ratio for a given file by identifying
        the stall statements contained within the file."""
        if nodes is None:
            return self._sr_detections
        with open(
            os.path.join(os.path.dirname(__file__), self._reference_file),
            "r",
            encoding="UTF-8",
        ) as file:
            reference = json.load(file)

        stall_visitor = StallVisitor(libcst_module, reference)
        wrapper_actual_file = libcst.metadata.MetadataWrapper(libcst_module)
        wrapper_actual_file.visit(stall_visitor)
        stall_dict = stall_visitor.get_stall_dict()

        for key, value in stall_dict.items():
            self._sr_detections[-1].append((key, value))

        # score_average = []
        # stall_total = 0
        # stall_ratio = 0
        # for node in nodes:
        # score = 0
        # Handle simple cases with pattern matching
        # lines = ast.unparse(node).splitlines()
        # for index, line in enumerate(lines):
        #     if any(stall in line for stall in reference[self._sr_access]):
        #         score += 1
        #         self._sr_detections[-1].append((node.lineno + index, line))

        # # Handle more complex cases for frivolous operations
        # for sub_node in ast.walk(node):
        #     if isinstance(sub_node, ast.BinOp):
        #         # Handle the case where 0 is being added or subtracted
        #         if isinstance(sub_node.op, (ast.Add, ast.Sub)) and (
        #             (
        #                 isinstance(sub_node.left, ast.Constant)
        #                 and sub_node.left.value == 0
        #             )
        #             or (
        #                 isinstance(sub_node.right, ast.Constant)
        #                 and sub_node.right.value == 0
        #             )
        #         ):
        #             score = self._complex_update_score(sub_node, score)
        #         # Handle the case where 1 is being multiplied or divided
        #         elif isinstance(
        #             sub_node.op, (ast.Mult, ast.Div, ast.FloorDiv)
        #         ) and (
        #             (
        #                 isinstance(sub_node.left, ast.Constant)
        #                 and sub_node.left.value == 1
        #             )
        #             or (
        #                 isinstance(sub_node.right, ast.Constant)
        #                 and sub_node.right.value == 1
        #             )
        #         ):
        #             score = self._complex_update_score(sub_node, score)
        #     elif isinstance(sub_node, ast.AugAssign):
        #         # Handle the case where 0 is being added or subtracted
        #         if (
        #             isinstance(sub_node.op, (ast.Add, ast.Sub))
        #             and isinstance(sub_node.value, ast.Constant)
        #             and sub_node.value.value == 0
        #         ):
        #             score = self._complex_update_score(sub_node, score)
        #         # Handle the case where 1 is being multiplied or divided
        #         elif (
        #             isinstance(sub_node.op, (ast.Mult, ast.Div, ast.FloorDiv))
        #             and isinstance(sub_node.value, ast.Constant)
        #             and sub_node.value.value == 1
        #         ):
        #             score = self._complex_update_score(sub_node, score)

        #     stall_total += score
        #     score_average.append(score / len(ast.unparse(node).split("\n")))

        # for score in score_average:
        #     stall_ratio += score
        # if len(score_average) > 0:
        #     stall_ratio = stall_ratio / len(score_average)
        # else:
        #     stall_ratio = 0

        return self._sr_detections

    def _complex_update_score(self, node, score):
        score += 1
        self._sr_detections[-1].append((node.lineno, ast.unparse(node)))
        return score


class StallVisitor(libcst.VisitorMetadataProvider):
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
                    print(f"stall statement '{line} found at line {actual_line}")
                    self._stall_dict[actual_line] = line

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
                    print(f"stall statement '{line} found at line {actual_line}")
                    self._stall_dict[actual_line] = line

    def get_score(self):
        return self._score

    def get_stall_dict(self):
        return self._stall_dict
