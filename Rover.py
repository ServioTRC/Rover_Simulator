from numpy.random import randint

X_CENTER_MOTHER_SHIP = 1
Y_CENTER_MOTHER_SHIP = 48
SAMPLE = 5
OBSTACLE = 1
JUMPS = 1


class Rover:

    SAMPLE_NUMBER = 11

    def __init__(self, x_limit, y_limit, name):
        self.has_rock = False
        self.name = name
        self.origin_path = []
        self.traces_number = 2
        self.position_x = X_CENTER_MOTHER_SHIP
        self.position_y = Y_CENTER_MOTHER_SHIP
        self.previous_steps = [(X_CENTER_MOTHER_SHIP, Y_CENTER_MOTHER_SHIP)]
        self.steps = 0
        self.x_limit = x_limit
        self.y_limit = y_limit
        self.preference = randint(0, 2)
        self.repeated = 0
        self.comming_home = False

    def change_position(self, data):
        prev_position_x, prev_position_y = self.position_x, self.position_y
        traces = False
        if self.has_rock or self.comming_home:
            return (prev_position_x, prev_position_y), (self.return_home()), traces
        else:
            evaded = self.evade_obstacle_directed(data)
            if data[self.position_y][self.position_x] == SAMPLE:
                data[self.position_y][self.position_x] = 7
                self.has_rock = True
                traces = True
            if evaded:
                self.previous_steps.append((self.position_x, self.position_y))
            return (prev_position_x, prev_position_y), (self.position_x, self.position_y), traces

    def return_home(self):
        if len(self.previous_steps) > 1:
            self.position_x, self.position_y = self.previous_steps.pop()
        else:
            if self.has_rock:
                print(f"{self.name} home and leaved sample")
                self.SAMPLE_NUMBER -= 1
                if self.SAMPLE_NUMBER <= 0:
                    raise AttributeError("No more samples")
                self.has_rock = False
            self.comming_home = False
            self.position_x, self.position_y = X_CENTER_MOTHER_SHIP, Y_CENTER_MOTHER_SHIP
        return self.position_x, self.position_y

    def evade_obstacle_directed(self, data):
        if self.preference == 0: # up
            if not self.move_front(data):
                return self.evade_obstacle_random(data)
        else: # right
            if not self.move_right(data):
                return self.evade_obstacle_random(data)
        return True

    def evade_obstacle_random(self, data):
        for _ in range(20):
            movement = randint(0, 4)
            if movement == 0 and self.move_left(data):
                return True
            elif movement == 1 and self.move_right(data):
                return True
            elif movement == 2 and self.move_front(data):
                return True
            elif movement == 3 and self.move_back(data):
                return True
        self.position_x, self.position_y = self.previous_steps.pop()
        self.repeated += 1
        if self.repeated > 4:
            self.comming_home = True
        return False

    def move_left(self, data):
        future_step = (self.position_x - JUMPS, self.position_y)
        if self.position_x - JUMPS >= 0 and future_step not in self.previous_steps and data[self.position_y][self.position_x - JUMPS] != OBSTACLE:
            self.position_x -= JUMPS
            return True
        return False

    def move_right(self, data):
        future_step = (self.position_x + JUMPS, self.position_y)
        if self.position_x + JUMPS < self.x_limit and future_step not in self.previous_steps and data[self.position_y][self.position_x + JUMPS] != OBSTACLE:
            self.position_x += JUMPS
            return True
        return False

    def move_front(self, data):
        future_step = (self.position_x, self.position_y - JUMPS)
        if self.position_y - JUMPS >= 0 and future_step not in self.previous_steps and data[self.position_y - JUMPS][self.position_x] != OBSTACLE:
            self.position_y -= JUMPS
            return True
        return False

    def move_back(self, data):
        future_step = (self.position_x, self.position_y + JUMPS)
        if self.position_y + JUMPS < self.y_limit and future_step not in self.previous_steps and data[self.position_y + JUMPS][self.position_x] != OBSTACLE:
            self.position_y += JUMPS
            return True
        return False

# Reducir el nivel de aleatoriedad de movimientos, mover al lugar mas alejado
# Siguen la misma direccion excepto cuando encuentran las migajas
