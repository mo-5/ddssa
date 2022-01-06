""" tests contains any unit tests for backend files
"""


class SRNone:
    """File contains 0 stall statements"""

    def __init__(self):
        self.factorial = 0

    def no_stall_method(self):
        """Method contains 0 stall statements"""
        for i in range(1, 5):
            self.factorial *= i
        print(self.factorial)

    def simple_method(self):
        """Method contains 0 stall statements"""
        print(self.factorial)
