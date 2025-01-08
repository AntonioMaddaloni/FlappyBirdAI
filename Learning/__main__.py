import gymnasium as gym
from stable_baselines3 import PPO

# Stampa tutti gli ambienti registrati
print("Ambienti registrati:", gym.envs.registry.keys())

# Assicurati che l'ambiente sia registrato
env = gym.make('FlappyBird-v0')

# Configura e addestra il modello PPO
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10)

# Salva il modello
model.save("ppo_flappybird")