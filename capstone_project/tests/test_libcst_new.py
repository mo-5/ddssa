import libcst
import libcst.metadata
import json
from capstone_project.backend.metrics.stall_visitor import StallVisitor
import unittest


class TestLibCST(unittest.TestCase):
    def setUp(self):
        self.value = None

    file_to_parse = "capstone_project/tests/static_test_files/sr_medium.py"

    with open(
        file_to_parse,
        "r",
        encoding="UTF-8",
    ) as file:
        file_contents = file.read()

    with open(
        "capstone_project/backend/metrics/stall_statements.json",
        "r",
        encoding="UTF-8",
    ) as file:
        reference = json.load(file)

    module = libcst.parse_module(file_contents)

    stall_visitor = StallVisitor(module, reference)
    wrapper_actual_file = libcst.metadata.MetadataWrapper(module)
    wrapper_actual_file.visit(stall_visitor)
    assert(stall_visitor.get_score() == 9)
