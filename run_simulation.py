import matplotlib.pyplot as plt
from matplotlib import colors
from numpy import genfromtxt
from matplotlib.animation import FuncAnimation
from Rover import (Rover, TWO_TRACES, ONE_TRACE,
                   EMPTY, MOTHER_SHIP, ROVER_MARK)


class Simulation:

    def __init__(self):
        self.data = genfromtxt('map.csv', delimiter=',')
        self.size = len(self.data)
        self.cmap = colors.ListedColormap(['white', 'brown', 'blue', 'orange', 'yellow', 'green', 'black', 'black'])
        self.bounds = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.norm = colors.BoundaryNorm(self.bounds, self.cmap.N)
        self.fig, self.ax = plt.subplots()
        self.rovers = [Rover(self.size, self.size, "guille"), Rover(self.size, self.size, "erick"),
                       Rover(self.size, self.size, "sergio"), Rover(self.size, self.size, "adrian"),
                       Rover(self.size, self.size, "pablo"), Rover(self.size, self.size, "yuso")]

    def draw_rovers(self):
        for rover in self.rovers:
            prev, actual, traces = rover.change_position(self.data)
            prev_x, prev_y = prev
            x, y = actual
            print(rover.name, x, y)
            if traces or self.data[y][x] == ONE_TRACE:
                self.data[y][x] = ONE_TRACE
            elif traces or self.data[y][x] == TWO_TRACES:
                self.data[y][x] = TWO_TRACES
            if not traces and self.data[y][x] != TWO_TRACES and self.data[y][x] != ONE_TRACE:
                self.data[y][x] = ROVER_MARK
            if rover.inside_mother(prev_x, prev_y):
                self.data[prev_y][prev_x] = MOTHER_SHIP
            elif self.data[prev_y][prev_x] == ONE_TRACE:
                self.data[prev_y][prev_x] = ONE_TRACE
            elif self.data[prev_y][prev_x] == TWO_TRACES:
                self.data[prev_y][prev_x] = TWO_TRACES
            else:
                self.data[prev_y][prev_x] = EMPTY

    def update(self, frame_number):
        self.ax.clear()
        self.ax.imshow(self.data, cmap=self.cmap, norm=self.norm)
        self.ax.tick_params(axis='both',
                            which='both',
                            bottom=False,
                            top=False,
                            labelbottom=False,
                            labelleft=False)
        self.draw_rovers()

    def run_simulation(self):
        try:
            animation = FuncAnimation(self.fig, self.update)
            plt.show()
        except AttributeError:
            print("All samples were found")


if __name__ == "__main__":
    simu = Simulation()
    simu.run_simulation()
