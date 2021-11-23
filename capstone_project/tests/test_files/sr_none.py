# File contains 0 stall statements

class SRNone:
    def __init__(self):
        pass

    def no_stall_method(self):
        factorial = 0
        for i in range(1, 5):
            factorial *= i
        print(factorial)