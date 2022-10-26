import gym 

myenv = gym.make('MultiCar-v0')

myenv.reset()
# Rendering our instance 300 times
for _ in range(300):
  #renders the environment
  myenv.render()
  #Takes a random action from its action space 
  # aka the number of unique actions an agent can perform
  myenv.step(myenv.action_space.sample())
  # env.step()
myenv.close()