import ast
import os
import json


class SRCalculator:
    """ SRCalculator is responsible for calculation the SR of
    loop statements.
    """
    def __init__(self, filename):
        self._filename = filename
        self._reference_file = "stall_statements.json"
        self._sr_access = "sr_statements"
        self._sr_detections = (self._filename, [])

    def set_filename(self, filename):
        self._filename = filename
        self._sr_detections = (self._filename, [])

    def calculate_sr(self, nodes):
        with open(os.path.join(os.path.dirname(__file__),
                               self._reference_file), "r") as f:
            reference = json.load(f)

        score = 0
        for node in nodes:
            print(node.lineno)
            # Handle simple cases with pattern matching
            lines = ast.unparse(node).split("\n")
            for line in lines:
                if any(stall in line for stall in reference[self._sr_access]):
                    score += 1
                    self._sr_detections[-1].append((node.lineno, line))

            # Handle more complex cases for frivolous operations
            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.BinOp):
                    # Handle the case where 0 is being added or subtracted
                    if isinstance(sub_node.op, (ast.Add, ast.Sub)):
                        if isinstance(sub_node.left, ast.Constant):
                            if sub_node.left.value == 0:
                                score += 1
                                self._sr_detections[-1].append(
                                    (node.lineno, ast.unparse(node)))
                        if isinstance(sub_node.right, ast.Constant):
                            if sub_node.right.value == 0:
                                score += 1
                                self._sr_detections[-1].append(
                                    (node.lineno, ast.unparse(node)))
                    # Handle the case where 1 is being multiplied or divided
                    elif isinstance(sub_node.op, (ast.Mult, ast.Div,
                                                  ast.FloorDiv)):
                        if isinstance(sub_node.left, ast.Constant):
                            if sub_node.left.value == 1:
                                score += 1
                                self._sr_detections[-1].append(
                                    (node.lineno, ast.unparse(node)))
                        if isinstance(sub_node.right, ast.Constant):
                            if sub_node.right.value == 1:
                                score += 1
                                self._sr_detections[-1].append(
                                    (node.lineno, ast.unparse(node)))
                elif isinstance(sub_node, ast.AugAssign):
                    # Handle the case where 0 is being added or subtracted
                    if isinstance(sub_node.op, (ast.Add, ast.Sub)):
                        if isinstance(sub_node.value, ast.Constant):
                            if sub_node.value.value == 0:
                                score +=1
                                self._sr_detections[-1].append(
                                    (node.lineno, ast.unparse(node)))
                    # Handle the case where 1 is being multiplied or divided
                    elif isinstance(sub_node.op, (ast.Mult, ast.Div,
                                                  ast.FloorDiv)):
                        if isinstance(sub_node.value, ast.Constant):
                            if sub_node.value.value == 1:
                                score +=1
                                self._sr_detections[-1].append(
                                    (node.lineno, ast.unparse(node)))


        print("File {} has {} number of stall statements".format(
            self._filename, score))
        return self._sr_detections
