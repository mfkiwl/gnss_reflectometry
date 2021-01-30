import time
import datetime
import re
import numpy


class Rinex:

    def __init__(self, file_path):
        self.path = file_path
        self.version = []
        self.station_name = []
        self.position = []
        self.types_G = []
        self.types_R = []
        self.types_E = []
        self.obs_G = []
        self.obs_R = []
        self.obs_E = []

    def parse_header(self):
        """parse line with header"""
        def set_version(line):
            if "RINEX VERSION" in line:
                self.version = line.split()[0]

        def set_station_name(line):
            if "NAME" in line:
                self.station_name = line.split()[0]

        def set_position(line):
            if "POSITION" in line:
                self.position = [line.split()[0], line.split()[1], line.split()[2]]

        def set_obs_type(line):
            def parse_types(line):
                line = line.split()[:-6]
                if line[0] == "G":
                    self.types_G = line[1:]
                if line[0] == "R":
                    self.types_R = line[1:]
                if line[0] == "E":
                    self.types_E = line[1:]
            if "OBS TYPES" in line:
                parse_types(line)

        file = open(self.path)
        line = file.readline()

        while "END OF HEADER" not in line:
            set_version(line)
            set_station_name(line)
            set_position(line)
            set_obs_type(line)
            line = file.readline()
        file.close()

    def parse_obs(self):
        file = open(self.path)
        line = file.readline()

        def get_time(line):
            year = int(line[0])
            month = int(line[1])
            day = int(line[2])
            hour = int(line[3])
            minute = int(line[4])
            second = int(line[5].split('.')[0])
            msecond = int(line[5].split('.')[1])
            epoch_time = datetime.datetime(year, month, day, hour, minute, second, msecond)
            return epoch_time

        def split_obs_line(line):
            line = line.replace('\n', '')
            line = line.split()
            if len(line[0]) == 1:
                line[0] = line[0] + " " + line.pop(1)
            return line
        while line:
            if line.startswith('>'):
                temp_l = line.replace('>', "").split()
                count_sat = int(temp_l[-1])
                epoch_time = get_time(temp_l)
                for i in range(count_sat):
                    line = file.readline()
                    if line[0].startswith('G'):
                        temp = [epoch_time]
                        temp.extend(split_obs_line(line))
                        self.obs_G.append(temp)
                    if line[0].startswith('R'):
                        temp = [epoch_time]
                        temp.extend(split_obs_line(line))
                        self.obs_R.append(temp)
                    if line[0].startswith('E'):
                        temp = [epoch_time]
                        temp.extend(split_obs_line(line))
                        self.obs_E.append(temp)
            line = file.readline()

    def get_epochs_count(self):
        return ["G:", len(self.obs_G), "R:", len(self.obs_R), "E:", len(self.obs_E)]




path = "data/rinex3.21o"
rinex = Rinex(path)

rinex.parse_header()
rinex.parse_obs()
print(rinex.get_epochs_count())



