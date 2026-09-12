import random

GRID_WIDTH = 20
GRID_HEIGHT = 20

class SnakeEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.food = self._spawn_food()
        self.done = False
        self.frame_count = 0
        return self._get_state()

    def _spawn_food(self):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in self.snake:
                return pos

    def _get_state(self):
        head_x, head_y = self.snake[0]
        dx, dy = self.direction

        point_l = (head_x - 1, head_y)
        point_r = (head_x + 1, head_y)
        point_u = (head_x, head_y - 1)
        point_d = (head_x, head_y + 1)

        dir_l = self.direction == (-1, 0)
        dir_r = self.direction == (1, 0)
        dir_u = self.direction == (0, -1)
        dir_d = self.direction == (0, 1)

        state = [
            (dir_r and self._is_collision(point_r)) or
            (dir_l and self._is_collision(point_l)) or
            (dir_u and self._is_collision(point_u)) or
            (dir_d and self._is_collision(point_d)),

            (dir_u and self._is_collision(point_r)) or
            (dir_d and self._is_collision(point_l)) or
            (dir_l and self._is_collision(point_u)) or
            (dir_r and self._is_collision(point_d)),

            (dir_d and self._is_collision(point_r)) or
            (dir_u and self._is_collision(point_l)) or
            (dir_r and self._is_collision(point_u)) or
            (dir_l and self._is_collision(point_d)),

            dir_l, dir_r, dir_u, dir_d,

            self.food[0] < head_x,
            self.food[0] > head_x,
            self.food[1] < head_y,
            self.food[1] > head_y,
        ]
        return [int(x) for x in state]

    def _is_collision(self, point):
        x, y = point
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return True
        if point in self.snake:
            return True
        return False

    def step(self, action):
        self.frame_count += 1

        clockwise = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        idx = clockwise.index(self.direction)

        if action == 0:
            new_dir = clockwise[idx]
        elif action == 1:
            new_dir = clockwise[(idx + 1) % 4]
        else:
            new_dir = clockwise[(idx - 1) % 4]

        self.direction = new_dir

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        reward = 0

        if self._is_collision(new_head) or self.frame_count > 100 * len(self.snake):
            self.done = True
            reward = -10
            return self._get_state(), reward, self.done

        self.snake.insert(0, new_head)

        if new_head == self.food:
            reward = 10
            self.food = self._spawn_food()
        else:
            self.snake.pop()

        return self._get_state(), reward, self.done