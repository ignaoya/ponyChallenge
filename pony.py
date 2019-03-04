import requests

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

def get_moves(pos, maze, width):
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
        moves = get_moves(i, maze, maze['size'][0])
        map_moves.append(moves)
    return map_moves

def find_route(maze):
    from random import choice, seed
    pos = maze['pony'][0]
    endpoint = maze['end-point'][0]
    maze_width = maze['size'][0]
    map_moves = get_full_map_moves(maze)
    domo = domokun_possible_pos(maze)
    route = []
    route_pos = []
    checkpoints = []
    pos = pos
    endpoint = endpoint
    from_checkpoint = False
    restart_checkpoint = False
    last_move = None
    paths_taken = []
    while pos != endpoint:
        print(pos, route, checkpoints)
        possible_moves = map_moves[pos]
        if len(possible_moves) > 2 or last_move is None and len(possible_moves) > 1:
            checkpoints.append({'pos': pos, 'moves': route.copy(), 'route_pos': route_pos.copy(),
                                'last_move': last_move, 'paths_taken': paths_taken.copy()}) 
            from_checkpoint = True
             
        if last_move == 'north':
            possible_moves = [x for x in possible_moves if x != 'south']
        if last_move == 'south':
            possible_moves = [x for x in possible_moves if x != 'north']
        if last_move == 'east':
            possible_moves = [x for x in possible_moves if x != 'west']
        if last_move == 'west':
            possible_moves = [x for x in possible_moves if x != 'east']
        if restart_checkpoint:
            possible_moves = [x for x in possible_moves if x in paths_taken]
            paths_taken = []
            restart_checkpoint = False

            
        if len(possible_moves) == 0 or pos in domo:
            searching = True
            while searching:
                route = checkpoints[-1]['moves'].copy()
                route_pos = checkpoints[-1]['route_pos'].copy()
                last_move = checkpoints[-1]['last_move']
                pos = checkpoints[-1]['pos']
                paths_taken = checkpoints[-1]['paths_taken'].copy()
                restart_checkpoint = True
                checkpoints.remove(checkpoints[-1])
                if len(paths_taken) + 1 < len(map_moves[pos]) or last_move is None:
                    searching = False
            continue
            
        move = choice(possible_moves)
        if from_checkpoint:
            checkpoints[-1]['paths_taken'].append(move)
            from_checkpoint = False
        route.append(move)
        last_move = move
        if move == 'north':
            pos -= maze_width
        elif move == 'south':
            pos += maze_width
        elif move == 'west':
            pos -= 1
        elif move == 'east':
            pos += 1
        route_pos.append(pos)
    return route, route_pos

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
    domo_map_moves = get_full_map_moves(maze)
    if 'north' in domo_map_moves[domo_pos]:
        possible_pos.append(domo_pos - maze_width)
    if 'south' in domo_map_moves[domo_pos]:
        possible_pos.append(domo_pos + maze_width)
    if 'west' in domo_map_moves[domo_pos]:
        possible_pos.append(domo_pos - 1)
    if 'east' in domo_map_moves[domo_pos]:
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
    start_game(maze_url, route, route_pos, maze)

