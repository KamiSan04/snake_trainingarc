# Snake RL 🐍

So this is a project where i built the classic snake game and then trained an AI to play it using reinforcement learning (specifically DQN - deep q network). Started as just wanting to make snake in pygame but then i got curious if i could make an AI learn to play it on its own, without me writing any strategy for it.

Spoiler: it actually works pretty well, AI hits scores of 60+ after couple thousand games of training lol.

## What's in here

- `game.py` - the actual playable snake game (pygame), you can play this with arrow keys
- `env.py` - same game but headless (no graphics) wrapped as an RL environment, this is what the AI trains on
- `model.py` - the neural network (small feedforward net, nothing fancy)
- `agent.py` - the agent logic, epsilon greedy exploration + training step
- `train.py` - run this to actually train the AI, it'll print scores as it goes
- `model.pth` - the saved weights of my trained model (best one so far)

## How it works (kinda)

Basically the AI doesnt see the game like we do, it doesnt get pixels or anything. instead i give it a simplified "state" - just 11 numbers that tell it stuff like:
- is there danger right in front/left/right of it
- what direction its currently moving
- where the food is relative to its head

Then it picks one of 3 moves (go straight, turn left, turn right) and gets a reward - +10 if it eats food, -10 if it dies. Over thousands of games it learns which moves lead to good rewards.

The "learning" part is a neural network that gets better and better at predicting which move is best given a state, this is the Q part of DQN (Q-learning).

## Running it

You'll need python (i used 3.11, pygame doesnt play nice with newer versions yet fyi) and these installed:

```
pip install -r requirements.txt
```

**To train the AI from scratch:**
```
python train.py
```
This runs forever basically, just Ctrl+C when your happy with the score. It'll save the model automatically whenever it beats its previous best score.

**To watch the trained AI play:**
```
python watch_ai.py
```
(needs model.pth to exist first, obviously)

## Some notes / things i learned

- pygame wouldnt install on my machine at first bc i had python 3.14 which is too new, had to downgrade to 3.11
- training can look "stuck" if the snake gets into an infinite loop (going in circles forever without dying) — had to add a step limit so episodes dont run forever
- scores dont improve in a straight line, its more like... up and down but trending up overall. record score keeps going up tho even when individual games are bad
- 11-value state instead of raw pixels made this WAY easier, network doesnt have to learn to "see" anything, just has to map simple numbers to good decisions

## Todo / ideas for later

- [ ] let training resume from saved model instead of starting over everytime  
- [ ] track score over time on a graph
- [ ] maybe try rewarding it for moving closer to food not just eating it
- [ ] see if bigger network / more layers helps at all

built this while learning RL basics, not an expert so if something looks weird in the code thats probably why lmao
