# File contains 8 stall statements

class SRAdvanced:
    def __init__(self):
        pass
        self.some_stuff = ["test", "test2", "test3"]

    def do_something(self):
        for stuff in self.some_stuff:
            print(stuff) #Stall
            for letter in stuff:
                count = 0
                count += 0 #Stall
                average = 1
                average = average / 1 #Stall
                count *= 1 #Stall
                print(average) #Stall
                logging.info(letter) #Stall

        for i in range(5):
            i += 0 #Stall
            print("new loop test for stall here as well") #Stall