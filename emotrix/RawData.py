import csv
import numpy as np


class RawData(object):
    def __init__(self, file_data="prueba.csv"):
        self.file_name = file_data
        reader = csv.reader(open(file_data, "rb"), delimiter='\t', quotechar='"')
        self.x = []
        self.F3 = []
        self.F4 = []
        self.AF3 = []
        self.AF4 = []
        self.tag = []

        for row in reader:
            if len(row) == 6:
                self.x.append(int(row[0]))
                self.F3.append(int(row[1].split(':')[1].split(',')[1]))
                self.F4.append(int(row[2].split(':')[1].split(',')[1]))
                self.AF3.append(int(row[3].split(':')[1].split(',')[1]))
                self.AF4.append(int(row[4].split(':')[1].split(',')[1]))
                self.tag.append(row[5])
        self.F3 = np.array(self.F3)
        self.F4 = np.array(self.F4)
        self.AF3 = np.array(self.AF3)
        self.AF4 = np.array(self.AF4)
        self.x = np.array(self.x)
        self.tag = np.array(self.tag)

    def get_divided_data(self):
        F3 = []
        F4 = []
        AF3 = []
        AF4 = []
        x = []
        tag = []
        before = self.tag[0]
        before_cont = 0
        i = 0
        cont_blocks = 1
        for t in self.tag:
            if t != before:
                if self.tag[i]:
                    F3.append(self.F3[before_cont:i])
                    F4.append(self.F4[before_cont:i])
                    AF3.append(self.AF3[before_cont:i])
                    AF4.append(self.AF4[before_cont:i])
                    x.append(self.x[before_cont:i])
                    tag.append(self.tag[before_cont:i])
                    before_cont = i
                    cont_blocks = 0
                cont_blocks += 1
                before = t
            i += 1
        print x
        return x, F3, F4, AF3, AF4, tag


    def get_F3(self):
        return self.F3

    def get_F4(self):
        return self.F4



