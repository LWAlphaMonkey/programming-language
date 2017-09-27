import sys
import os
import re
import copy

'''booth arrangement'''
FILE_PATH = os.path.dirname(os.path.abspath(__file__))

class FileLoader:
    def get_param(self, file_name):
        ret = {}
        ret['dimension'] = {}
        ret['position'] = {}
        ret['target'] = {}
        fp = open(FILE_PATH + '/' + file_name, 'r')
        lines = fp.readlines()
        fp.close()

        for line in lines:
            input_type = line[:line.index('(')]
            content = [int(re.search(r'\d+', elem).group()) for elem in list(line.split(','))]
            
            if input_type == 'booths':
                ret['booths'] = content[0]
            elif input_type == 'dimension' or input_type == 'position':
                ret[input_type][content[0]] = [content[1], content[2]]
            elif input_type == 'target':
                ret[input_type] = Target(content[0], [content[1], content[2]])
            else:
                ret[input_type] = [val for val in content]

        return ret

class Booth:
    def __init__(self, booth_id, dim, pos):
        '''dimension[w][h],pos[y][x]'''
        self.id = booth_id
        self.dimension = dim
        self.position = pos

class Target:
    def __init__(self, target_id, pos):
        self.id = target_id
        self.position = pos

class Room:
    def __init__(self, dim, booths, target, horizon):
        width = dim[0]
        height = dim[1]
        self.room = [[0 for x in range(0, width)] for y in range(0, height)]
        self.width = width
        self.height = height
        self.booths = booths
        self.target = target
        self.move = horizon
        self.final_room = copy.deepcopy(self.room)

    def set_room(self, prm):
        for idx in range(1, prm['booths'] + 1):
            pos = prm['position'][idx]

            if idx == self.target.id:
                pos = self.target.position

            self.add_booth(idx, prm['dimension'][idx], prm['position'][idx], self.room)            
            self.add_booth(idx, prm['dimension'][idx], pos, self.final_room)

    def add_booth(self, booth_id, size, pos, destination):
        for x in range(pos[0], pos[0] + size[0]):
            for y in range(pos[1], pos[1] + size[1]):
                destination[y][x] = booth_id

    def add_booth_to_dummy_room(self, room, pos):
        for x in range(pos[0], pos[0] + BOOTHS[0].dimension[0]):
            for y in range(pos[1], pos[1] + BOOTHS[0].dimension[1]):
                if room[y][x] == 0:
                    room[y][x] = VISITED
        
        return room

    def get_booth_position(self, room, booth_id):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if room[y][x] == booth_id:
                    return [x, y]

    def move_booth(self, room, booth_id, booth_dim, visited):
        ret = []
        is_target = booth_id == self.target.id
        booth_pos = self.get_booth_position(room, booth_id)
        min_x, max_x = booth_pos[0], booth_pos[0] + booth_dim[0] - 1
        min_y, max_y = booth_pos[1], booth_pos[1] + booth_dim[1] - 1
        up, down, left, right = max_y + 1, min_y - 1, min_x - 1, max_x + 1
        visited_pos = [visited]
        dummy_room = copy.deepcopy(room)
        update_info = 0

        if is_target:
            visited_pos.append([min_x, min_y])
        
        # move up        
        if up < self.height and max_x < self.width:
            target_pos = [dummy_room[up][x] for x in range(min_x, max_x + 1)]
            check_condition = all(val == 0 for val in target_pos)
            
            if check_condition:
                ret_room = copy.deepcopy(dummy_room)       

                for x in range(min_x, max_x + 1):
                    for y in range(min_y, up + 1):
                        if y == min_y:
                            ret_room[y][x] = update_info
                        else: 
                            ret_room[y][x] = booth_id
                ret.append(ret_room)

        # move down
        if down >= 0 and max_x < self.width and max_y < self.height:
            target_pos = [dummy_room[down][x] for x in range(min_x, max_x + 1)]
            check_condition = all(val == 0 for val in target_pos)

            if check_condition:
                ret_room = copy.deepcopy(dummy_room)       
                
                for x in range(min_x, max_x + 1):
                    for y in range(down, max_y + 1):
                        if y == max_y:
                            ret_room[y][x] = update_info
                        else: 
                            ret_room[y][x] = booth_id
                
                ret.append(ret_room) 
        
        # movee left
        if left >= 0 and max_x < self.width and max_y < self.height:
            target_pos = [dummy_room[y][left] for y in range(min_y, max_y + 1)]
            check_condition = all(val == 0 for val in target_pos)
            
            if check_condition:
                ret_room = copy.deepcopy(dummy_room)

                for x in range(left, max_x + 1):
                    for y in range(min_y, max_y + 1):
                        if x == max_x:
                            ret_room[y][x] = update_info
                        else: 
                            ret_room[y][x] = booth_id
                
                ret.append(ret_room)

        # move right
        if right < self.width and max_y < self.height:
            target_pos = [dummy_room[y][right] for y in range(min_y, max_y + 1)]
            check_condition = all(val == 0 for val in target_pos)
            
            if check_condition:
                ret_room = copy.deepcopy(dummy_room)

                for x in range(min_x, right + 1):
                    for y in range(min_y, max_y + 1):
                        if x == min_x:
                            ret_room[y][x] = update_info
                        else: 
                            ret_room[y][x] = booth_id
                
                ret.append(ret_room)

        return [ret,visited_pos]    

    def move_bfs(self, room, booths, count, visited):
        arranged_room = []
        count += 1
        
        if count >= self.move:
            return False

        # get all possible move
        for booth in booths:
            tmp = self.move_booth(room, booth.id, booth.dimension, visited)
            for idx, new_room in enumerate(tmp[0]):
                try:
                    arranged_room.append([new_room, tmp[1][idx]])
                except:
                    arranged_room.append([new_room, []])

        # judge result
        for possible_room in arranged_room:
            target_pos = self.get_booth_position(possible_room[0], self.target.id)
            if target_pos == self.target.position:
                if possible_room[0] == self.final_room and self.move > count:
                    self.move = count
                else:
                    for booth in booths:
                        if booth.id != self.target.id:
                            self.reset_bfs(possible_room[0], booths, count, [])
                        
                return True
            else:
                self.move_bfs(possible_room[0], booths, count, possible_room[1])

    def reset_bfs(self, room, booths, count, visited):
        arranged_room = []
        count += 1
        
        if count >= self.move:
            return False

        # get all possible move
        for booth in booths:
            if booth.id != self.target.id:
                tmp = self.move_booth(room, booth.id, booth.dimension, visited)
                for idx, new_room in enumerate(tmp[0]):
                    try:
                        arranged_room.append([new_room, tmp[1][idx]])
                    except:
                        arranged_room.append([new_room, []])

        # judge result
        for possible_room in arranged_room:
            if possible_room[0] == self.final_room:
                if self.move > count:
                    self.move = count
                
                return True
            else:
                self.reset_bfs(possible_room[0], booths, count, possible_room[1])

def main():
    prm = {}
    booths = []

    try:
        prm = FileLoader().get_param(sys.argv[1])        
    except:
       print("please enter an inputFile")
       return False

    room = Room(prm['room'], prm['booths'], prm['target'], prm['horizon'][0])
    room.set_room(prm)
    booths.append(Booth(room.target.id, [0,0], [0,0]))    
    
    for idx in range(1, room.booths + 1):
        if idx == room.target.id:
            booths[0].position = prm['position'][idx]
            booths[0].dimension = prm['dimension'][idx]
        else:
            booths.append(Booth(idx, prm['dimension'][idx], prm['position'][idx]))
    
    room.move_bfs(room.room, booths, 0, [])    
    print('moves(' + str(room.move) + ').')
    
    return True
    
if __name__ == '__main__':
    main()