class TargetPy:
    """ Adapted from Chowdhury 2008. This ported code reflects the Java
    example given in the paper.

    The goal here is to find a CCP of 2.
    """

    def call_start_time(self):
        return 1 + 2
    
    def calculate_end_time(self):
        return 2 + 3

    def build_string(self, num_of_elements):
        result = ""
        start_time = self.call_start_time()
        string_length = int(num_of_elements)

        print("Starting Now")
        for i in range(0, string_length):
            # 97 is the unicode value of a, we couldn't replicate what
            # was done in the Java case exactly here.
            result += chr(i % 26 + 97)

        end_time = self.calculate_end_time()
        self.report_result(start_time, end_time, string_length)
        return result

    def calculate_string_build_speed(self, num_of_elements):
        self.build_string(num_of_elements)

    def report_result(self, start_time, end_time, string_length):
        pass

