import ast


class SRCalculator:
    """ SRCalculator is responsible for calculation the SR of
    loop statements.
    """
    def __init__(self, filename):
        self._filename = filename
        # TODO Use JSON instead for this.
        self._reference_file = "stall_statements.txt"

    def set_filename(self, filename):
        self._filename = filename

    def calculate_sr(self, nodes):
        reference = []
        with open(self._reference_file, "r") as f:
            reference = f.readline().split(",")

        score = 0
        for node in nodes:
            lines = ast.unparse(node).split("\n")
            for line in lines:
                # TODO discuss if multiple statements per line would
                #   be grounds to increment SR multiple times.
                if any(stall in line for stall in reference):
                    score += 1
        print("File {} has a calculated stall ratio of {}".format(
            self._filename, score))



if __name__ == '__main__':
    sr = SRCalculator("Test")
    sr.calculate_sr(None)
