from env import SnakeEnv

env = SnakeEnv()
state = env.reset()
print("Initial state:", state)

state, reward, done = env.step(0)
print("After one step:", state, reward, done)