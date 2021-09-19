import os


class CCPParserPy:
    """ The goal of this class is to parse data from a target Python
    file and then use said data to calculate the maximum CCP of the
    class while providing the name of the method that produced that
    max CCP value
    """

    def collect_method_names(self, target_file):
        names = []
        with open(target_file) as f:
            for line in f.readlines():
                if "def" in line and line.strip()[0:4] == "def ":
                    names.append(line.split("(")[0].split(" ")[-1])
        return names

    def parameters_per_method(self, method_name, target_file):
        with open(target_file) as f:
            for line in f.readlines():
                if "def" in line and method_name in line \
                        and line.strip()[0:4] == "def ":
                    return line.split("(")[-1].strip(
                        "self").strip(",").split(")")[0].strip(" ")


def parse_target_file(path):
    method_names = ccp_tester.collect_method_names(path)
    print("Number of methods: " + str(len(method_names)))
    print("Method names:")
    for name in method_names:
        print("\t" + name)
    for i in range(len(method_names)):
        print("Parameter(s) in method {}".format(method_names[i]))
        parameters = ccp_tester.parameters_per_method(
            method_names[i], path)
        if len(parameters) == 0:
            print("\tNo parameters (0)")
        else:
            print("\t{} ({})".format(parameters, len(parameters.split(","))))


if __name__ == '__main__':
    ccp_tester = CCPParserPy()
    file_path = os.path.join(os.getcwd(), "SamplePythonFiles", "target_py.py")
    file_path_2 = os.path.join(
        os.getcwd(), "SamplePythonFiles", "test_zoia_py.py")

    print("Test 1: target_py.py")
    parse_target_file(file_path)

    print("\nTest 2: test_zoia_py.py")
    parse_target_file(file_path_2)
