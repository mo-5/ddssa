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

    def set_filename(self, filename):
        self._filename = filename

    def calculate_sr(self, nodes):
        with open(os.path.join(os.path.dirname(__file__),
                               self._reference_file), "r") as f:
            reference = json.load(f)

        score = 0
        for node in nodes:
            lines = ast.unparse(node).split("\n")
            for line in lines:
                # TODO discuss if multiple statements per line would
                #   be grounds to increment SR multiple times.
                if any(stall in line for stall in reference[self._sr_access]):
                    score += 1
        print("File {} has a calculated stall ratio of {}".format(
            self._filename[-1], score))
