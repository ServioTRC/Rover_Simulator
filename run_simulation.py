import matplotlib.pyplot as plt
from matplotlib import colors
from numpy import genfromtxt
from matplotlib.animation import FuncAnimation
from Rover import (Rover, TWO_TRACES, ONE_TRACE,
                   EMPTY, MOTHER_SHIP, ROVER_MARK)

data = genfromtxt('map.csv', delimiter=',')
size = len(data)
cmap = colors.ListedColormap(['white', 'brown', 'blue', 'orange', 'yellow', 'green', 'black', 'black'])
bounds = [0, 1, 2, 3, 4, 5, 6, 7, 8]
norm = colors.BoundaryNorm(bounds, cmap.N)
fig, ax = plt.subplots()
rovers = [Rover(size, size, "guille"), Rover(size, size, "erick"),
          Rover(size, size, "sergio"), Rover(size, size, "adrian"),
          Rover(size, size, "pablo"), Rover(size, size, "yuso")]


def draw_rovers():
    for rover in rovers:
        prev, actual, traces = rover.change_position(data)
        prev_x, prev_y = prev
        x, y = actual
        print(rover.name, x, y)
        if traces or data[y][x] == ONE_TRACE:
            data[y][x] = ONE_TRACE
        elif traces or data[y][x] == TWO_TRACES:
            data[y][x] = TWO_TRACES
        if not traces and data[y][x] != TWO_TRACES and data[y][x] != ONE_TRACE:
            data[y][x] = ROVER_MARK
        if rover.inside_mother(prev_x, prev_y):
            data[prev_y][prev_x] = MOTHER_SHIP
        elif data[prev_y][prev_x] == ONE_TRACE:
            data[prev_y][prev_x] = ONE_TRACE
        elif data[prev_y][prev_x] == TWO_TRACES:
            data[prev_y][prev_x] = TWO_TRACES
        else:
            data[prev_y][prev_x] = EMPTY


def update(frame_number):
    ax.clear()
    ax.imshow(data, cmap=cmap, norm=norm)
    ax.tick_params(axis='both',
                   which='both',
                   bottom=False,
                   top=False,
                   labelbottom=False,
                   labelleft=False)
    draw_rovers()


try:
    animation = FuncAnimation(fig, update)
    plt.show()
except AttributeError:
    pass
