import random
from collections import namedtuple

import matplotlib.pyplot as plt
import pandas as pd

# Type Model for cell show
# param x: pos  x
# param y: pos  y
# param z: count of this pos and size of point in figure.
# for simple,we choose two-dimension to show population
Point = namedtuple('Point', ['x', 'y', 'z'])


def cell_copy(point: Point) -> Point:
    # to express a new cell, give it a position.
    standard_bias = 2
    bias_x = random.randint(-standard_bias, standard_bias)
    bias_y = random.randint(-standard_bias, standard_bias)
    # random direction as cell propagation method
    return Point(x=point.x + bias_x, y=point.y + bias_y, z=1)


def change_to_DataFrame(result: dict) -> pd.DataFrame:
    _result = pd.DataFrame(result.items(), columns=['pos', 'z'])
    _result['x'] = _result['pos'].map(lambda x: int(x.split('_')[0]))
    _result['y'] = _result['pos'].map(lambda x: int(x.split('_')[1]))
    del _result['pos']
    _result = _result.sort_values(by=['x', 'y'])  # sort value by (x,y) for picture show in order.
    return _result


def combine_key(point: Point) -> str:
    return '_'.join([str(point.x), str(point.y)])


def propagation(bio_set: dict) -> dict:
    next_period_cells = {}
    for key, value in bio_set.items():
        # two method to implement probability:
        # first: choose 20% cell to discard, the other divide.
        # two:   for every cell, give 20% probability to discard.
        choice = random.randint(0, 10)  # produce [1-10]
        if choice < 3:  # 20% percent probability discard
            bio_set[key] = value - 1 if value > 0 else 0  # set flag for discard later.
            continue

        new_point = cell_copy(Point(x=int(key.split('_')[0]), y=int(key.split('_')[1]), z=1))
        key_str = combine_key(new_point)
        if key_str in bio_set:
            bio_set[key_str] += 1  # cell count of this position incr 1
        else:
            next_period_cells[key_str] = 1
    return next_period_cells


if __name__ == '__main__':

    # choose dict as a map struct for simplicity, redis is more reasonable solution when you consider large memory.
    bio_set = {}
    start = Point(0, 0, 1)  # first single cell，position (0,0,0) for pretty
    bio_set[str(start.x) + '_' + str(start.y)] = start.z
    period = 50  # supposed propagation period
    fig, ax = plt.subplots()
    for step in range(period):
        print('period:', step)

        new_dict = propagation(bio_set)
        bio_set.update(new_dict)
        # discard cell which is dead
        bio_set = {key: value for key, value in bio_set.items() if value > 0}

        period_result = change_to_DataFrame(bio_set)
        ax.scatter(x=period_result['x'], y=period_result['y'], s=period_result.z * 20, c='r')
        # a.plot(kind='scatter', x='x', y='y', s=a.z * 10, c='r')

        plt.xlim((-period, period))
        plt.ylim((-period, period))
        plt.xlabel('X')
        ax.text(34, 40, '{}th period'.format(step + 1))
        plt.ylabel('Y')
        plt.pause(0.01)
        ax.cla()
    plt.show()
