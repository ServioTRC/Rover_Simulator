import matplotlib.pyplot as plt
from matplotlib import colors
from numpy import genfromtxt
from matplotlib.animation import FuncAnimation
from Rover import Rover

data = genfromtxt('map.csv', delimiter=',')
size = len(data)
# create discrete colormap
cmap = colors.ListedColormap(['white', 'brown', 'blue', 'orange', 'yellow', 'green', 'black', 'black'])
bounds = [0, 1, 2, 3, 4, 5, 6, 7, 8] # Intervalos para cada uno de lo colorres 0-1 rojo, 1-2 azul
norm = colors.BoundaryNorm(bounds, cmap.N)
fig, ax = plt.subplots()


rovers = [Rover(size, size, "guille"), Rover(size, size, "erick"), Rover(size, size, "sergio"), Rover(size, size, "adrian")]
# rovers = [Rover(size, size, "guille")]


def inside_mother(x, y):
    return x == 1 and y == 48


def draw_rovers():
    for rover in rovers:
        prev, actual, traces = rover.change_position(data)
        prev_x, prev_y = prev
        x, y = actual
        print(rover.name, x, y)
        if traces or data[y][x] == 7 or data[y][x] == 8:
            data[y][x] = 7
        elif traces or data[y][x] == 8:
            data[y][x] = 8
        else:
            data[y][x] = 3
        if inside_mother(prev_x, prev_y):
            data[prev_y][prev_x] = 2
        elif data[prev_y][prev_x] == 7:
            data[prev_y][prev_x] = 7
        elif data[prev_y][prev_x] == 8:
            data[prev_y][prev_x] = 8
        else:
            data[prev_y][prev_x] = 0


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
