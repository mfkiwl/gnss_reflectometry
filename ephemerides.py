import datetime
import pandas as pd


class Ephemerides:
    def __init__(self, path):
        self.path = path


class Sp3(Ephemerides):
    def __init__(self, path):
        self.data = []
        self.path = path

    def parse_sp3(self):
        file = open(self.path)
        line = file.readline()
        data = []
        while line:
            if line.startswith('*'):
                line = line.split()
                year = int(line[1])
                month = int(line[2])
                day = int(line[3])
                hour = int(line[4])
                minutes = int(line[5])
                second = int(line[6].split('.')[0])
                msecond = int(float(line[6].split('.')[1]) * 1000)
                time = datetime.datetime(year, month, day, hour, minutes, second, msecond)
                line = file.readline()
                while line.startswith('P'):
                    line = line.split()
                    data.append([time, line[0], line[1], line[2], line[3], line[4]])
                    line = file.readline()

        self.data = pd.DataFrame(data, columns=['data', 'sat', 'x', 'y', 'z', 't'])

    def print_data(self):
        for i in self.data:
            print(i)

    def getXYZ_in_time(self, sat, time):
        print(self.data[self.data["sat"] == sat])


eph = Sp3('data/test.sp3')
eph.parse_sp3()
eph.getXYZ_in_time('PC01',0)
#eph.print_data()
#print(eph.data)


