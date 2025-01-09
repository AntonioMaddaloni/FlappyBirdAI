import gymnasium as gym
from FlappyBird_Gym.__main__ import FlappyBirdEnv  #Assicurati che questo percorso sia corretto
import random

#Crea l'ambiente FlappyBird
env = FlappyBirdEnv()
done = False
#initilize
obs = env.reset()
#Ciclo di gioco con azioni casuali
while True:
    #Seleziona un'azione casuale
    if not done:
        action = random.choice([0, 1])
    print(action)
    # Esegui un passo nell'ambiente
    obs, reward, done, truncated, info = env.step(action)
    print(obs)
    # Renderizza l'ambiente
    env.render()

# Chiudi l'ambiente
env.close()

random.choice([0, 1])