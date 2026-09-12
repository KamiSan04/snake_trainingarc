import torch
from model import QNetwork

net = QNetwork()
dummy_state = torch.tensor([0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1], dtype=torch.float32)
output = net(dummy_state)
print(output)