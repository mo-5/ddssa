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
        if filename is None:
            raise TypeError
        self._filename = filename
        self._sr_detections = (self._filename, [])

    def calculate_sr(self, nodes):
        if nodes is None:
            return self._sr_detections
        with open(
                os.path.join(os.path.dirname(__file__), self._reference_file), "r"
        ) as file:
            reference = json.load(file)

        score_average = []
        stall_total = 0
        stall_ratio = 0
        for node in nodes:
            score = 0
            # Handle simple cases with pattern matching
            lines = ast.unparse(node).splitlines()
            for index, line in enumerate(lines):
                if any(stall in line for stall in reference[self._sr_access]):
                    score += 1
                    self._sr_detections[-1].append((node.lineno + index, line))

            # Handle more complex cases for frivolous operations
            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.BinOp):
                    # Handle the case where 0 is being added or subtracted
                    if isinstance(sub_node.op, (ast.Add, ast.Sub)) and (
                            (
                                    isinstance(sub_node.left, ast.Constant)
                                    and sub_node.left.value == 0
                            )
                            or (
                                    isinstance(sub_node.right, ast.Constant)
                                    and sub_node.right.value == 0
                            )
                    ):
                        score = self._complex_update_score(sub_node, score)
                    # Handle the case where 1 is being multiplied or divided
                    elif isinstance(
                            sub_node.op, (ast.Mult, ast.Div, ast.FloorDiv)
                    ) and (
                            (
                                    isinstance(sub_node.left, ast.Constant)
                                    and sub_node.left.value == 1
                            )
                            or (
                                    isinstance(sub_node.right, ast.Constant)
                                    and sub_node.right.value == 1
                            )
                    ):
                        score = self._complex_update_score(sub_node, score)
                elif isinstance(sub_node, ast.AugAssign):
                    # Handle the case where 0 is being added or subtracted
                    if (
                            isinstance(sub_node.op, (ast.Add, ast.Sub))
                            and isinstance(sub_node.value, ast.Constant)
                            and sub_node.value.value == 0
                    ):
                        score = self._complex_update_score(sub_node, score)
                    # Handle the case where 1 is being multiplied or divided
                    elif (
                            isinstance(sub_node.op, (ast.Mult, ast.Div, ast.FloorDiv))
                            and isinstance(sub_node.value, ast.Constant)
                            and sub_node.value.value == 1
                    ):
                        score = self._complex_update_score(sub_node, score)

            stall_total += score
            score_average.append(score / len(ast.unparse(node).split("\n")))

        for score in score_average:
            stall_ratio += score
        if len(score_average) > 0:
            stall_ratio = stall_ratio / len(score_average)
        else:
            stall_ratio = 0

        # logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
        # logging.info(
        #     f"File {self._filename} has {stall_ratio} " f"total stall statements"
        # )
        # logging.info(
        #     f"File {self._filename} "
        #     f"has a calculated average stall ratio of {stall_ratio}"
        # )
        # logging.info(self._sr_detections)
        return self._sr_detections

    def _complex_update_score(self, node, score):
        score += 1
        self._sr_detections[-1].append((node.lineno, ast.unparse(node)))
        return score