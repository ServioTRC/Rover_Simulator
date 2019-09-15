from numpy.random import randint
from matplotlib.pyplot import pause

X_CENTER_MOTHER_SHIP = 1
Y_CENTER_MOTHER_SHIP = 48
SAMPLE = 5
OBSTACLE = 1
TWO_TRACES = 8
ONE_TRACE = 7
EMPTY = 0
MOTHER_SHIP = 2
ROVER_MARK = 3


class Rover:

    def __init__(self, x_limit, y_limit, name, sample_number, jumps=1, max_step_directed=1):
        self.has_rock = False
        self.name = name
        self.position_x = X_CENTER_MOTHER_SHIP
        self.position_y = Y_CENTER_MOTHER_SHIP
        self.previous_steps = [(X_CENTER_MOTHER_SHIP, Y_CENTER_MOTHER_SHIP)]
        self.steps = 0
        self.x_limit = x_limit
        self.y_limit = y_limit
        self.preference = randint(0, 3)
        self.repeated = 0
        self.comming_home = False
        self.sample_number = sample_number
        self.jumps = jumps
        self.max_step_directed = max_step_directed

    def change_position(self, data):
        prev_position_x, prev_position_y = self.position_x, self.position_y
        traces = False
        if self.has_rock or self.comming_home:
            return (prev_position_x, prev_position_y), (self.return_home()), traces
        else:
            self.steps += self.jumps
            if self.steps > self.max_step_directed:
                self.steps = 0
                evaded = self.evade_obstacle_random(data)
            else:
                evaded = self.evade_obstacle_directed(data)
            if data[self.position_y][self.position_x] == SAMPLE:
                print(f"{self.name} found sample at X:{self.position_x} Y:{self.position_y}")
                data[self.position_y][self.position_x] = TWO_TRACES
                self.has_rock = True
                traces = True
            elif data[self.position_y][self.position_x] == TWO_TRACES:
                print(f"{self.name} found traces at X:{self.position_x} Y:{self.position_y}")
                data[self.position_y][self.position_x] = ONE_TRACE
                self.change_direction(prev_position_x, prev_position_y)
            elif data[self.position_y][self.position_x] == ONE_TRACE:
                print(f"{self.name} found traces at X:{self.position_x} Y:{self.position_y}")
                data[self.position_y][self.position_x] = EMPTY
                self.change_direction(prev_position_x, prev_position_y)
            if evaded:
                self.previous_steps.append((self.position_x, self.position_y))
            return (prev_position_x, prev_position_y), (self.position_x, self.position_y), traces

    def return_home(self):
        if len(self.previous_steps) > 1:
            self.position_x, self.position_y = self.previous_steps.pop()
        else:
            self.preference = randint(0, 3)
            if self.has_rock:
                self.sample_number[0] -= 1
                print(f"{self.name} is home and left sample. Missing to find {self.sample_number[0]} samples")
                if self.sample_number[0] <= 0:
                    print("All samples found")
                    pause(30)
                    exit()
                self.has_rock = False
                self.preference = randint(0, 2)
            self.comming_home = False
            self.position_x, self.position_y = X_CENTER_MOTHER_SHIP, Y_CENTER_MOTHER_SHIP
        return self.position_x, self.position_y

    def evade_obstacle_directed(self, data):
        if self.preference == 0:    # up
            if not self.move_up(data):
                return self.evade_obstacle_random(data)
        elif self.preference == 1:
            if not self.move_up_right(data):
                return self.evade_obstacle_random(data)
        else:   # right
            if not self.move_right(data):
                return self.evade_obstacle_random(data)
        return True

    def evade_obstacle_random(self, data):
        for _ in range(20):
            movement = randint(0, 8)
            if movement == 0 and self.move_left(data):
                return True
            elif movement == 1 and self.move_right(data):
                return True
            elif movement == 2 and self.move_up(data):
                return True
            elif movement == 3 and self.move_down(data):
                return True
            elif movement == 4 and self.move_up_left(data):
                return True
            elif movement == 5 and self.move_up_right(data):
                return True
            elif movement == 6 and self.move_down_left(data):
                return True
            elif movement == 7 and self.move_down_right(data):
                return True
        self.position_x, self.position_y = self.previous_steps.pop()
        self.repeated += 1
        if self.repeated > 4:
            self.comming_home = True
        return False

    def move_left(self, data):
        future_step = (self.position_x - self.jumps, self.position_y)
        if self.position_x - self.jumps >= 0 and future_step not in self.previous_steps and data[self.position_y][self.position_x - self.jumps] != OBSTACLE:
            self.position_x -= self.jumps
            return True
        return False

    def move_right(self, data):
        future_step = (self.position_x + self.jumps, self.position_y)
        if self.position_x + self.jumps < self.x_limit and future_step not in self.previous_steps and data[self.position_y][self.position_x + self.jumps] != OBSTACLE:
            self.position_x += self.jumps
            return True
        return False

    def move_up(self, data):
        future_step = (self.position_x, self.position_y - self.jumps)
        if self.position_y - self.jumps >= 0 and future_step not in self.previous_steps and data[self.position_y - self.jumps][self.position_x] != OBSTACLE:
            self.position_y -= self.jumps
            return True
        return False

    def move_down(self, data):
        future_step = (self.position_x, self.position_y + self.jumps)
        if self.position_y + self.jumps < self.y_limit and future_step not in self.previous_steps and data[self.position_y + self.jumps][self.position_x] != OBSTACLE:
            self.position_y += self.jumps
            return True
        return False

    def move_up_right(self, data):
        return self.move_up(data) and self.move_right(data)

    def move_up_left(self, data):
        return self.move_up(data) and self.move_left(data)

    def move_down_right(self, data):
        return self.move_down(data) and self.move_right(data)

    def move_down_left(self, data):
        return self.move_down(data) and self.move_left(data)

    def change_direction(self, previous_x, previous_y):
        if previous_x != self.position_x and previous_y != self.position_y:
            self.preference = 2
        if previous_x != self.position_x:
            self.preference = 1
        elif previous_y != self.position_y:
            self.preference = 0

    def inside_mother(self, x, y):
        return x == X_CENTER_MOTHER_SHIP and y == Y_CENTER_MOTHER_SHIP
