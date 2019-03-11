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

def find_route(maze):
    pony = maze['pony'][0]
    endpoint = maze['end-point'][0]
    domo = domokun_possible_pos(maze)


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

