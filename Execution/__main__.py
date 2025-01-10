import gymnasium as gym
from stable_baselines3 import PPO

# Crea l'ambiente
env = gym.make('FlappyBird-v0')

# Carica il modello
model = PPO.load("./Models/ppo_flappybird")

# Inizializza l'ambiente
obs, info = env.reset()  # Gymnasium restituisce una tupla (obs, info)
done = False

while not done:
    # Usa solo `obs` per il modello
    action, _ = model.predict(obs)
    print(action)
    # Esegui un passo nell'ambiente
    obs, reward, done, truncated, info = env.step(action)

    # Renderizza l'ambiente
    env.render()

# Chiudi l'ambiente
env.close()