import requests
from random import choice

url = 'https://ponychallenge.trustpilot.com/pony-challenge/maze'

data = {"maze-width": 15,
        "maze-height":15,
        "maze-player-name": "Applejack",
        "difficulty": 0}

def get_maze_id(url, data):
    try:
        r = requests.post(url = url, json = data)
        failed_conn = False
    except: 
        failed_conn = True
    while failed_conn or r.status_code != 200:
        print("#get_maze_id# Failed connection. Retrying...")
        try:
            r = requests.post(url=url, json=data)
            failed_conn = False
        except: 
            failed_conn = True
    return r

def get_maze_state(maze_url):
    try:
        r = requests.get(url = maze_url)
        failed_conn = False
    except:
        failed_conn = True
    while failed_conn or r.status_code != 200:
        print("#get_maze_state# Failed connection. Retrying...")
        try:
            r = requests.get(url = maze_url)
            failed_conn = False
        except:
            failed_conn = True
    return r.json()

def get_moves(pos, maze):
    width = maze['size'][0]
    moves = []
    if 'west' not in maze['data'][pos]:
        moves.append('west')
    if 'north' not in maze['data'][pos]:
        moves.append('north')
    if pos + 1 < len(maze['data']) and 'west' not in maze['data'][pos + 1]:
        moves.append('east')
    if (pos + width) < len(maze['data']) and 'north' not in maze['data'][pos + width]:
        moves.append('south')
    return moves

def get_full_map_moves(maze):
    map_moves = []
    for i in range(len(maze['data'])):
        moves = get_moves(i, maze)
        map_moves.append(moves)
    return map_moves

def change_pos(pos, maze_width, direction):
    if direction == 'north':
        return pos - maze_width
    elif direction == 'south':
        return pos + maze_width
    elif direction == 'east':
        return pos + 1
    elif direction == 'west':
        return pos - 1

def determine_orientation(pos, maze):
    endpoint = maze['end-point'][0]
    width = maze['size'][0]
    orientation = []
    if endpoint %  width > pos % width:
        orientation.append('east')
    if endpoint % width < pos % width:
        orientation.append('west')
    if endpoint > pos + (width - (pos % width)) - 1:
        orientation.append('south')
    if endpoint < pos - (pos % width):
        orientation.append('north')
    return orientation

def clean_moves(moves, last_move)
    if last_move == 'north':
        moves.remove('south')
    if last_move == 'south':
        moves.remove('north')
    if last_move == 'east':
        moves.remove('west')
    if last_move == 'west':
        moves.remove('east')
    return moves

def find_route(maze):
    width = maze['size'][0]
    pos = maze['pony'][0]
    endpoint = maze['end-point'][0]
    domo = domokun_possible_pos(maze)
    map_moves = get_full_map_moves(maze)
    route = []
    checkpoints = []
    last_move = None
    paths_taken = []
    while pos != endpoint:
        orientation = determine_orientation(pos, maze)
        possible_moves = clean_moves(map_moves[pos], last_move)
        if len(possible_moves) > 1:
            checkpoints.append({'pos': pos, 'route': route.copy(), 'last_move': last_move, 'paths_taken': []})
        if len(possible_moves) == 0:
            pos = checkpoints[-1]['pos']
            route = checkpoints[-1]['route'].copy()
            last_move = checkpoints[-1]['last_move']
            paths_taken = checkpoints[-1]['paths_taken'].copy()
            continue
        if paths_taken:
            for i in paths_taken:
                possible_moves.remove(i)
            paths_taken = []
        if any((i for i in possible_moves if i in orientation)):
            for i in possible_moves:
                if i in orientation:
                    route.append(i)
                    pos = change_pos(pos, width, i)
        else:
            move = choice(possible_moves)
            route.append(i)
            pos = change_pos(pos, width, i)




def post_move(maze_url, move):
    data = {'direction': move}
    failed_conn = False
    try:
        r = requests.post(url = maze_url, json = data)
    except:
        failed_conn = True
    while failed_conn or r.status_code != 200:
        print("Failed connection. Retrying...")
        try:
            r = requests.pos(url=maze_url, json = data)
            failed_conn = False
        except:
            failed_conn = True

def domokun_possible_pos(maze):
    domo_pos = maze['domokun'][0]
    maze_width = maze['size'][0]
    possible_pos = [domo_pos]
    domo_moves = get_moves(domo_pos, maze)
    if 'north' in domo_moves:
        possible_pos.append(domo_pos - maze_width)
    if 'south' in domo_moves:
        possible_pos.append(domo_pos + maze_width)
    if 'west' in domo_moves:
        possible_pos.append(domo_pos - 1)
    if 'east' in domo_moves:
        possible_pos.append(domo_pos + 1)
    return possible_pos



def start_game(maze_url, route, route_pos, maze):
    pos = maze['pony'][0]
    endpoint = maze['end-point'][0]
    while pos != endpoint:
        maze = get_maze_state(maze_url)
        domo = domokun_possible_pos(maze)
        if any(set(domo).intersection(route_pos)):
           route, route_pos = find_route(maze) 
        post_move(maze_url, route.pop(0))
        pos = route_pos.pop(0)


if __name__ == '__main__':
    maze_id = get_maze_id(url, data).json()["maze_id"]
    maze_url = '/'.join([url, maze_id])
    maze = get_maze_state(maze_url)
    route, route_pos = find_route(maze)
    #start_game(maze_url, route, route_pos, maze)

