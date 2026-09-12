from env import SnakeEnv
from agent import Agent

def train():
    agent = Agent()
    env = SnakeEnv()
    record = 0

    while True:
        state_old = env._get_state()
        final_move = agent.get_action(state_old)
        action = final_move.index(1)

        state_new, reward, done = env.step(action)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            score = len(env.snake) - 1
            env.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.save()

            print(f"Game {agent.n_games}, Score: {score}, Record: {record}")

if __name__ == "__main__":
    train()