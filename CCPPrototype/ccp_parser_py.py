import os


class CCPParserPy:
    """ The goal of this class is to parse data from a target Python
    file and then use said data to calculate the maximum CCP of the
    class while providing the name of the method that produced that
    max CCP value.
    """

    def __init__(self, path):
        """ Initialize the class for a specific Python class file.

        :param path: The Python class file that will be analyzed.
        """
        self.method_names = []
        self.target_file = path

    def collect_method_names(self):
        """ Collect all of the method names in a passed python file.

        :return: The names of each method located in target_file, as a
                 list
        """
        names = []
        with open(self.target_file) as f:
            for line in f.readlines():
                if line.strip()[0:4] == "def ":
                    names.append(line.split("(")[0].split(" ")[-1])
        self.method_names = names
        return names

    def parameters_per_method(self, method_name):
        """ Return a list of parameters associated with a specific
        method name.

        :param method_name: The method that will have its parameters
                            collected.
        :return: A striped list of the parameters for the method.
        """
        with open(self.target_file) as f:
            for line in f.readlines():
                if method_name in line and line.strip()[0:4] == "def ":
                    return line.split("(")[-1].strip(
                        "self").strip(",").split(")")[0].strip(" ")

    def parse_out_methods(self):
        """ Return a dict of method definitions keyed by their name.
        These methods are parsed out of a specific Python class file.
        Untested, but this should work regardless of whether the file
        makes use of classes.

        :return: A dict of method def'n keyed by their method name.
        """
        first_method = False
        line_no = -1
        start_line = 0
        curr_method = ""
        methods_dict = {}
        with open(self.target_file) as f:
            lines = f.readlines()
            for line in lines:
                line_no = line_no + 1
                if first_method is False and line.strip()[0:4] == "def ":
                    # Start of the method, figure out which
                    for name in self.method_names:
                        if name in line:
                            # Start of the method
                            first_method = True
                            start_line = line_no
                            curr_method = name
                elif line.strip()[0:4] == "def ":
                    # start of next method.
                    methods_dict[curr_method] = \
                        lines[start_line:line_no - 1]
                    start_line = line_no
                    for name in self.method_names:
                        if name in line:
                            curr_method = name
            # end of file, add last method
            methods_dict[curr_method] = lines[start_line:line_no + 1]
        print(methods_dict)
        return methods_dict

    def guess_ccp(self, method_dict):
        """ Attempts to guess the CCP for each method within a target
        file.

        :param method_dict: A dictionary with method names as a key
                            and their definition stored as a list
                            as the value.
        """
        # This entire method needs to be re-written but it was just
        # to have something for the presentation today. It really isn't
        # finished but the data to figure this out should exist thanks
        # to the other parsing methods.
        # TODO Don't forget the recursive case so the application stops.
        for method in self.method_names:
            ccp = 0
            curr_method = method_dict[method]
            parent_method = method
            curr_params = []
            for line in curr_method[1:]:
                for methods in self.method_names:
                    if method != methods and "self." in line and methods in line:
                        # Find parameters
                        # print(line)
                        # curr_params = str(line).split(
                        #    "(")[1].split(",").split(")")[0]
                        ccp += 1

            print("The CCP for the method {} is {}".format(parent_method, ccp))


def parse_target_file():
    method_names = ccp_tester.collect_method_names()
    print("Number of methods: " + str(len(method_names)))
    print("Method names:")
    for name in method_names:
        print("\t" + name)
    method_dict = {}
    for i in range(len(method_names)):
        print("Parameter(s) in method {}".format(method_names[i]))
        parameters = ccp_tester.parameters_per_method(
            method_names[i])
        if len(parameters) == 0:
            print("\tNo parameters (0)")
            method_dict[method_names[i]] = 0
        else:
            print("\t{} ({})".format(parameters, len(parameters.split(","))))
            method_dict[method_names[i]] = parameters
    ccp_tester.guess_ccp(ccp_tester.parse_out_methods())


if __name__ == '__main__':
    file_path = os.path.join(os.getcwd(), "SamplePythonFiles", "target_py.py")
    file_path_2 = os.path.join(
        os.getcwd(), "SamplePythonFiles", "test_zoia_py.py")
    ccp_tester = CCPParserPy(file_path)

    print("Test 1: target_py.py")
    parse_target_file()

    # ccp_tester = CCPParserPy(file_path_2)
    # print("\nTest 2: test_zoia_py.py")
    # parse_target_file(file_path_2)
