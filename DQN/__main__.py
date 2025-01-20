import gymnasium as gym
from stable_baselines3 import DQN

# Stampa tutti gli ambienti registrati
print("Ambienti registrati:", gym.envs.registry.keys())

# Assicurati che l'ambiente sia registrato
env = gym.make('FlappyBird-v0')

# Configura e addestra il modello PPO
model = DQN("MlpPolicy", env, verbose=1, batch_size=256,buffer_size=32768)
# Carica il modello salvato
#model = PPO.load("./Models/ppo_flappybird", env=env)
#addestramento
model.learn(total_timesteps=1000000)

# Salva il modello
model.save("./Models/dqn_flappybird")