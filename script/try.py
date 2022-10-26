import gym
import mujoco
#Setting Humanoid-v4 as the environment
# env = gym.make('InvertedPendulum-v4', ctrl_cost_weight=0.1)
env = gym.make('InvertedPendulum-v4')
#Sets an initial state
env.reset()
# Rendering our instance 300 times
for _ in range(1000):
  #renders the environment
  env.render()
  #Takes a random action from its action space 
  # aka the number of unique actions an agent can perform
  env.step(env.action_space.sample())
  # env.step()
env.close()