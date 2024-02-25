"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the environment part of this example.
The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""
import numpy as np
import time
import sys
from test import a_star
from numpy.core.numeric import Inf, Inf
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

UNIT = 10   # pixels
MAZE_H = 30  # grid height
MAZE_W = 50  # grid width
n=1


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()

        self.best_path,self.reward,self.station_dict,self.station_pos2id,self.C=a_star()
        self.nowstate=np.array(self.best_path[0][0])
        self.action_space = [str(i) for i in range(len(self.station_dict)-1)]
        self.n_actions = len(self.action_space)
        self.n_features = 2
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self._build_maze()

    def get_cost(self):
        return self.C

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        origin = np.array(self.best_path[0][0])


        # hell
        hell1_center = n*(np.array(origin))
        print("origin is:",origin)
        self.hell1 = self.canvas.create_rectangle(
            hell1_center[0] - 5, hell1_center[1] - 5,
            hell1_center[0] + 5, hell1_center[1] + 5,
            fill='black')
        # hell
        # hell2_center = origin + np.array([UNIT, UNIT * 2])
        # self.hell2 = self.canvas.create_rectangle(
        #     hell2_center[0] - 15, hell2_center[1] - 15,
        #     hell2_center[0] + 15, hell2_center[1] + 15,
        #     fill='black')

        # create oval
        # for _,v in self.station_dict.items():
        #     helln_center=n*(np.array(v))
            # print(v)
            # self.canvas.create_rectangle(
            #     helln_center[0] - 5, helln_center[1] - 5,
            #     helln_center[0] + 5, helln_center[1] + 5,
            #     fill='blue')

        oval_center =n*(np.array(self.best_path[-1][0]))
        print("oval is:",self.best_path[-1][0])
        self.oval =self.canvas.create_oval(
            oval_center[0] - 5, oval_center[1] - 5,
            oval_center[0] + 5, oval_center[1] + 5,
            fill='yellow')

        # create red rect
        self.rect = self.canvas.create_rectangle(
            origin[0] - 5, origin[1] - 5,
            origin[0] + 5, origin[1] + 5,
            fill='red')

        # pack all
        self.canvas.pack()

    def reset(self):

        self.update()
        time.sleep(0.1)
        self.canvas.delete(self.rect)
        self.nowstate=np.array(self.best_path[0][0])
        origin =n*( np.array(self.best_path[0][0]))
        self.rect = self.canvas.create_rectangle(
            origin[0] - 5, origin[1] - 5,
            origin[0] + 5, origin[1] + 5,
            fill='red')
        # return observation
        return self.nowstate

    def step(self, action):
        s = self.nowstate
        base_action = np.array([0, 0])
        # if action == 0:   # up
        #     if s[1] > UNIT:
        #         base_action[1] -= UNIT
        # elif action == 1:   # down
        #     if s[1] < (MAZE_H - 1) * UNIT:
        #         base_action[1] += UNIT
        # elif action == 2:   # right
        #     if s[0] < (MAZE_W - 1) * UNIT:
        #         base_action[0] += UNIT
        # elif action == 3:   # left
        #     if s[0] > UNIT:
        #         base_action[0] -= UNIT
        base_action[0]=n*(np.array(self.station_dict[str(action)][0]))
        base_action[1] = n*(np.array(self.station_dict[str(action)][1]))
        # print("moving")

        self.canvas.move(self.rect,base_action[0], base_action[1])  # move agent
        # print("起始基站：",self.best_path[0][1])
        # print("当前基站：", self.nowstate)

        # self.rect = self.canvas.create_rectangle(
        #     base_action[0] - 5, base_action[1] - 5,
        #     base_action[0] + 5, base_action[1] + 5,
        #     fill='red')
        next_coords = np.array(self.station_dict[str(action)]) # next state
        id=self.station_pos2id[str(self.nowstate)]
        # print("下一基站：",action)
        # print("目的基站:",self.best_path[-1][1])
        # reward function
        if list(self.nowstate) ==list(next_coords):
            reward=0
            done=False
        elif list(self.nowstate)==list(np.array(self.best_path[-1][0])):
            reward=1-self.C[id][self.best_path[-1][1]]
            done=True
        else:
            reward = 1-self.C[id][action]
            done = False
        self.nowstate =np.array(self.station_dict[str(action)])
        # print("reward is:",reward)
        s_ = np.array(self.station_dict[str(action)])
        return s_, reward, done,self.C

    def render(self):
        # time.sleep(0.01)
        self.update()


