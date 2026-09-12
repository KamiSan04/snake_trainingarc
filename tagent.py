from agent import Agent

agent = Agent()
dummy_state = [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1]
action = agent.get_action(dummy_state)
print(action)