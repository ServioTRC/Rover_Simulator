import matplotlib.pyplot as plt
from matplotlib import colors
from numpy import genfromtxt
from matplotlib.animation import FuncAnimation
from Rover import (Rover, TWO_TRACES, ONE_TRACE,
                   EMPTY, MOTHER_SHIP, ROVER_MARK)


class Simulation:

    def __init__(self):
        self.sample_number = [9]
        self.data = genfromtxt('map.csv', delimiter=',')
        self.size_x = len(self.data)
        self.size_y = len(self.data[0])
        self.cmap = colors.ListedColormap(['white', 'brown', 'blue', 'orange', 'yellow', 'green', 'black', 'black'])
        self.bounds = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.norm = colors.BoundaryNorm(self.bounds, self.cmap.N)
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.set_window_title('Rover Simulator')
        self.rovers = [Rover(self.size_x, self.size_y, "guille", self.sample_number, jumps=1, max_step_directed=2),
                       Rover(self.size_x, self.size_y, "erick", self.sample_number, jumps=1, max_step_directed=2),
                       Rover(self.size_x, self.size_y, "sergio", self.sample_number, jumps=1, max_step_directed=2),
                       Rover(self.size_x, self.size_y, "adrian", self.sample_number, jumps=1, max_step_directed=2),
                       Rover(self.size_x, self.size_y, "pablo", self.sample_number, jumps=1, max_step_directed=2),
                       Rover(self.size_x, self.size_y, "yuso", self.sample_number, jumps=1, max_step_directed=2)]

    def draw_rovers(self):
        for rover in self.rovers:
            prev, actual, traces = rover.change_position(self.data)
            prev_x, prev_y = prev
            x, y = actual
            print(f"Rover Name: {rover.name} X:{x} Y:{y}")
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
        animation = FuncAnimation(self.fig, self.update)
        plt.show()


if __name__ == "__main__":
    simu = Simulation()
    simu.run_simulation()
