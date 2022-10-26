from gym.envs.registration import register
from MyEnvs.envs.MultiCarEnv import MultiCarEnv
register(
    id='MultiCar-v0',
    entry_point='MyEnvs.envs:MultiCarEnv',
    max_episode_steps=1000,
)
