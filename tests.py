import unittest
from pony import *

class TestGetMazeId(unittest.TestCase):

    def setUp(self):
        self.request = get_maze_id(url, data)
    
    def test_status_code_200(self):
        self.assertEqual(self.request.status_code, 200)

    def test_maze_id_in_json(self):
        self.assertIn('maze_id', self.request.json())

class TestGetMazeState(unittest.TestCase):

    def setUp(self):
        self.request = get_maze_id(url, data)
        self.maze_url = '/'.join([url, self.request.json()['maze_id']])
        self.maze = get_maze_state(self.maze_url)
    
    def test_state_active(self):
        self.assertEqual(self.maze['game-state']['state'], 'Active', f"Active is not {self.maze['game-state']['state']}")

    def test_pony_not_in_endpoint(self):
        self.assertNotEqual(self.maze['pony'], self.maze['end-point'])

class TestGetMoves(unittest.TestCase):

    def setUp(self):
        self.maze = {'data':[['north','west'],['north','west'],['west'],[]]}
        self.width = 2

    def test_west(self):
        pos_a = 3
        pos_b = 2

        moves_a = get_moves(pos_a, self.maze, self.width)
        moves_b = get_moves(pos_b, self.maze, self.width)

        self.assertIn('west', moves_a)
        self.assertNotIn('west', moves_b)

    def test_north(self):
        pos_a = 2
        pos_b = 0

        moves_a = get_moves(pos_a, self.maze, self.width)
        moves_b = get_moves(pos_b, self.maze, self.width)

        self.assertIn('north', moves_a)
        self.assertNotIn('north', moves_b)

    def test_east(self):
        pos_a = 2
        pos_b = 0

        moves_a = get_moves(pos_a, self.maze, self.width)
        moves_b = get_moves(pos_b, self.maze, self.width)

        self.assertIn('east', moves_a)
        self.assertNotIn('east', moves_b)

    def test_south(self):
        pos_a = 0
        pos_b = 2

        moves_a = get_moves(pos_a, self.maze, self.width)
        moves_b = get_moves(pos_b, self.maze, self.width)

        self.assertIn('south', moves_a)
        self.assertNotIn('south', moves_b)

if __name__ == '__main__':
    unittest.main()
