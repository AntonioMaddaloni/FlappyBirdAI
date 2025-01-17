from gymnasium.envs.registration import register

register(
    id='FlappyBird-v0',
    entry_point='FlappyBird_Gym.__main__:FlappyBirdEnv',
)