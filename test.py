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
        request = get_maze_id(url, data)
        maze_url = '/'.join([url, request.json()['maze_id']])
        self.maze = get_maze_state(maze_url)
    
    def test_status_code_200(self):
        self.assertEqual(self.maze['game-state']['state'], 'Active', f"active is not {self.maze['game-state']}")

if __name__ == '__main__':
    unittest.main()
