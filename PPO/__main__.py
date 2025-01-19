import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor

# Directory per i log
log_dir = './Logs/'

# Stampa tutti gli ambienti registrati
print("Ambienti registrati:", gym.envs.registry.keys())

# Assicurati che l'ambiente sia registrato
env = gym.make('FlappyBird-v0')

# Avvolgi l'ambiente con Monitor per registrare i dati
env = Monitor(env, './Logs/')  # Logs sarà la directory dove verranno salvati i dati di addestramento

# Configura e addestra il modello PPO
#model = PPO("MlpPolicy", env, verbose=1, batch_size=256,n_steps=32768)
# Carica il modello salvato
model = PPO.load("./Models/ppo_flappybird", env=env)
#addestramento
model.learn(total_timesteps=1000000)

# Salva il modello
model.save("./Models/ppo_flappybird")

# Chiudi l'ambiente
env.close()
