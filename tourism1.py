import sys
import os
import re
import time
import itertools as it

'''tourism1
Given a set L of locations, and partial rankings R = [R1, ..., Rn],
we want to find the ordering of L which is most consistent with R.
That is, the ordering of L which minimizes the sum of the number 
times each partial ranking is violated. Note that if several people 
have a violated preference, it is counted for each person.
Similarly, preferences are transitive: so given a ranking [1, 2, 3], 
the ordering [3, 2, 1] has 3 violations.
'''

#constant
FILE_PATH = os.path.dirname(os.path.abspath(__file__))

#global variable
_violation = 10000

class FileLoader:
    def get_param(self, file_name):
        ret = {}
        ret['order'] = []
        ret['people'] = {}
        fp = open(FILE_PATH + '/' + file_name, 'r')
        lines = fp.readlines()
        fp.close()

        for line in lines:
            if line != '\n':
                input_type = line[:line.index('(')]
                content = [int(re.search(r'\d+', elem).group()) for elem in list(line.split(','))]

                if input_type == 'people':
                    for i in range(1, content[0] + 1):
                        ret[input_type][i]=[]
                elif input_type == 'locations' or input_type == 'preferences':
                    ret[input_type] = content[0]
                elif input_type == 'order':
                    ret['people'][content[0]].append((str(content[1]), str(content[2])))
        return ret

def gen_preference_table(num):
    s = ''
    return list(map(''.join, it.permutations(''.join(str(val) for val in range(1, num+1)))))

def get_comparison_pair(people):
    preference = list(people)
    count = 0

    for pref in preference:
        for pref_1 in preference:
            if (pref[1] == pref_1[0]) and ((pref[0], pref_1[1]) not in preference):
                preference.append((pref[0], pref_1[1]))
            elif (pref[0] == pref_1[1]) and ((pref_1[0], pref[0]) not in preference):
                preference.append((pref_1[0],pref[0]))
                count +=1

    return {'count':count, 'preference': preference}

def get_all_comparison(people):
    ret = get_comparison_pair(people)
    
    while True:
        if ret['count'] == 0:
            break
        else:
            ret = get_comparison(ret['preference'])

    return ret['preference']

def check_violation(table, people):
    global _violation
    count = 0

    for tourism in people:
        all_comparison = get_all_comparison(people[tourism])
        for case in all_comparison:
            if table.index(case[0]) > table.index(case[1]):
                count += 1

    if _violation > count:
        _violation = count

def testcase():
    possible_preference = []
    ts = {}
    ts = FileLoader().get_param('tour1_5.lp.txt')
    
    tables = gen_preference_table(ts['locations'])
    for table in tables:
        check_violation(table, ts['people'])
    
    print(_violation)

def main():
    tourism1 = {}
    t_start = time.time()
    
    try:
        tourism1 = FileLoader().get_param(sys.argv[1])        
    except:
       print("please enter an inputFile")
       return False

    tables = gen_preference_table(tourism1['locations'])
    
    for table in tables:
        check_violation(table, tourism1['people'])
    
    print('violations(' + str(_violation) + ')')
    
    t_end = time.time()
    print("it costs %f sec" %(t_end - t_start))
    return True

if __name__ == '__main__':
    main()
