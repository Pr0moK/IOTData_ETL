
class datarange:
    def __init__(self):
        self.month = ""
        self.day = ""
        self.datatype =""

    def collect_data(self,typ):
        if typ == 1:
            self.month = input("Type month (1-5): ")
        if typ == 2:
            self.month = input("Type month (1-5): ")
            self.day = input("Type day: ")
        if typ == 3:
            self.datatype = input("1. Mean\n2. Max\n3. Min\nType: ")
        if typ == 4:
            self.month = input("Type month (1-5): ")
            self.day = input("Type day: ")

