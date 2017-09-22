import sys
import os
import re
import itertools

FILE_PATH = os.path.dirname(os.path.abspath(__file__))

class FileLoader:
    def get_param(self, file_name):
        ret = {}
        ret['order'] = []
        fp = open(FILE_PATH + '/' + file_name, 'r')
        lines = fp.readlines()
        fp.close()

        for line in lines:
            if line != '\n':
                input_type = line[:line.index('(')]
                content = [int(re.search(r'\d+', elem).group()) for elem in list(line.split(','))]

                if input_type == 'people' or input_type == 'places' or input_type == 'preferences':
                    ret[input_type] = content[0]
                else:
                    ret[input_type].append(ORDER(content[0], str(content[1], str(content[2]))))

        return ret

class ORDER:
    def __init__(self, people, loc_1, loc_2):
        self.people = people
        self.prefer_loc1 = loc_1
        self.prefer_loc2 = loc_2

def testcase():
    pass

def main():
    testcase()

if __name__ == '__main__':
    main()
