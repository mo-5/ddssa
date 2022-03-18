import libcst
import libcst.metadata
import json


def main():

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

    class StallVisitor(libcst.VisitorMetadataProvider):
        METADATA_DEPENDENCIES = (libcst.metadata.WhitespaceInclusivePositionProvider,)

        def __init__(self):
            self.score = 0
            self.stall_dict = {}

        def visit_For_body(self, node) -> None:
            pos = self.get_metadata(
                libcst.metadata.WhitespaceInclusivePositionProvider, node
            ).start
            lines = module.code_for_node(node).splitlines()
            for index, line in enumerate(lines):
                if any(stall in line for stall in reference["sr_statements"]):
                    if (pos.line + index) not in self.stall_dict:
                        self.score += 1
                        pos = self.get_metadata(
                            libcst.metadata.WhitespaceInclusivePositionProvider, node
                        ).start
                        actual_line = int(str(pos.line)) + index
                        print(
                            f"stall statement '{line} found at actual line {actual_line}"
                        )
                        self.stall_dict[actual_line] = line

        def visit_While_body(self, node) -> None:
            pos = self.get_metadata(
                libcst.metadata.WhitespaceInclusivePositionProvider, node
            ).start
            lines = module.code_for_node(node).splitlines()
            for index, line in enumerate(lines):
                if any(stall in line for stall in reference["sr_statements"]):
                    if (pos.line + index) not in self.stall_dict:
                        self.score += 1
                        actual_line = pos.line + index
                        print(f"stall statement '{line} found at line {actual_line}")
                        self.stall_dict[actual_line] = line

        def get_score(self):
            print(self.stall_dict)
            return self.score

    stall_visitor = StallVisitor()
    wrapper_actual_file = libcst.metadata.MetadataWrapper(module)
    wrapper_actual_file.visit(stall_visitor)
    print("Total number of stall statements: " + str(stall_visitor.get_score()))


if __name__ == "__main__":
    main()
