""" tests contains any unit tests for backend files
"""

import logging


class SRAdvanced:
    """File contains 8 stall statements"""

    def __init__(self):
        self.some_stuff = ["test", "test2", "test3"]

    def do_something(self):
        """Method contains 6 stall statements"""
        for stuff in self.some_stuff:
            print(stuff)  # Stall
            for letter in stuff:
                count = 0
                count += 0  # Stall
                average = 1
                average = average / 1  # Stall
                count *= 1  # Stall
                print(average)  # Stall
                logging.info(letter)  # Stall

    def do_something_else(self):
        """Method contains 2 stall statements"""
        print(self.some_stuff)
        for i in range(5):
            i += 0  # Stall
            print("new loop test for stall here as well")  # Stall
