import sys
import os
import re
import copy
import itertools as it

#constant
FILE_PATH = os.path.dirname(os.path.abspath(__file__))

class FileLoader:
    def get_param(self, file_name):
        ret = {}
        ret['locations'] = {}
        ret['people'] = {}
        fp = open(FILE_PATH + '/' + file_name, 'r')
        lines = fp.readlines()
        fp.close()

        for line in lines:
            if line != '\n':
                input_type = line[:line.index('(')]
                content = [int(re.search(r'\d+', elem).group()) for elem in list(line.split(','))]

                if input_type == 'people':
                    for idx in range(1, content[0] + 1):
                        ret[input_type][idx]= []
                elif input_type == 'locations':
                    ret['location_number'] = content[0]
                    for idx in range(1, content[0] + 1):
                        ret[input_type][idx] = []
                elif input_type == 'preferences':
                    ret[input_type] = content[0]
                elif input_type == 'location':
                    ret['locations'][content[0]]= {'D':content[1], 'O':content[2], 'C':content[3]}
                elif input_type == 'prefer':
                    ret['people'][content[0]].append(content[1])

        return ret

class TOOLS:
    def compare_number(self, satisfied_pair):
        satisfied_num = -1
        nonsatisfied_num = -1
        for single in satisfied_pair:
            if single[0] == True and single[1] > satisfied_num:
                satisfied_num = single[1]
            if single[0] == False:
                if nonsatisfied_num == -1:
                    nonsatisfied_num = single[1]
                else:
                    if single[1] < nonsatisfied_num:
                        nonsatisfied_num = single[1]

        if nonsatisfied_num == -1:
            ret = satisfied_num
        else:
            ret = nonsatisfied_num

        return ret

class SCHEDULE:
    def gen_preference_table(self, num):
        s = ''
        return list(map(''.join, it.permutations(''.join(str(val) for val in range(1, num + 1)))))

    def set_first_schedule(self, time_table, locations):
        possible_time_table = []

        for idx_x in locations:
            tmp_time_table = copy.deepcopy(time_table)
            duration_x = locations[idx_x].get('D')
            opening_x = locations[idx_x].get('O')
            
            for visit_hour in range(opening_x, opening_x + duration_x):
                tmp_time_table[visit_hour] = idx_x
            possible_time_table.append(tmp_time_table)

        return possible_time_table

    def set_rest_schedule(self, time_table, locations, count):
        ret_time_table = copy.deepcopy(time_table)

        for time in time_table:
            if count == 1:
                ret_time_table.remove(time)

            for idx in locations:
                available_hour = 0
                duration = locations[idx].get('D')
                opening = locations[idx].get('O')
                closing = locations[idx].get('C')
                tmp_time_table = copy.deepcopy(time)

                if (idx not in time.values()) and (sum(val == 0 for val in time.values()) >= duration):
                    for empty_time in range(opening, closing):
                        if time[empty_time] == 0:
                            available_hour += 1

                        if available_hour == duration:
                            for set_schedule in range(empty_time, empty_time - duration, -1):
                                tmp_time_table[set_schedule] = idx
                            if tmp_time_table not in ret_time_table:
                                ret_time_table.append(tmp_time_table)

        count += 1

        return {'count': count, 'table': ret_time_table}

    def get_time_duration(self, locations):
        opening = 24
        closing = 0
        time_table = {}

        for idx in locations:
            tmp_opening = locations[idx].get('O')
            tmp_closing = locations[idx].get('C')
            if tmp_opening < opening:
                opening = tmp_opening
            if tmp_closing > closing:
                closing = tmp_closing

        for hour in range(opening, closing):
            time_table[hour] = 0

        return time_table

    def get_schedule(self, time_table, locations, location_number):
        possible_time_table = self.set_first_schedule(time_table, locations)

        ret = self.set_rest_schedule(possible_time_table, locations, 1)
        
        while ret['count'] != location_number:
            ret = self.set_rest_schedule(ret['table'], locations, ret['count'])

        return ret['table']

    def check_satisfaction(self, tables, people):
        full_satisfied = []
        current_satisfied = 0
        max_satisfied = 0

        for table in tables:
            full_satisfied = []
            for person in people:
                current_satisfied = 0
                for prefer in people[person]:
                    if prefer in table.values():
                        current_satisfied += 1
                if current_satisfied == len(people[person]):
                    full_satisfied.append([True, current_satisfied])
                    if current_satisfied > max_satisfied:
                        max_satistied = current_satisfied
                else:
                    full_satisfied.append([False, current_satisfied])

            num = TOOLS().compare_number(full_satisfied)
            if num > max_satisfied:
                max_satisfied = num

        return max_satisfied

def main():
    schedule = SCHEDULE()

    try:
        tourism2 = FileLoader().get_param(sys.argv[1])        
    except:
       print("please enter an inputFile")
       return False

    possible_schedule = schedule.get_schedule(schedule.get_time_duration(tourism2['locations']),\
                                              tourism2['locations'],\
                                              tourism2['location_number'])
    count = schedule.check_satisfaction(possible_schedule, tourism2['people'])

    print('satisfaction(' + str(count) + ').')

    return True

if __name__ == '__main__':
    main()
