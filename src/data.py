import csv

class DriverData:
    def __init__(self, filename):
        self.drivers = {}
        self.load_data(filename)

    def load_data(self, filename):
        with open(filename, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                self.drivers[row[1]] = (int(row[2]), float(row[3]))

    def get_drivers(self):
        return self.drivers


class ConstructorData:
    def __init__(self, filename):
        self.constructors = {}
        self.load_data(filename)

    def load_data(self, filename):
        with open(filename, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                self.constructors[row[0]] = (int(row[1]), float(row[2]))

    def get_constructors(self):
        return self.constructors