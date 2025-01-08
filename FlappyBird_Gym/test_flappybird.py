import gymnasium as gym
from main import FlappyBirdEnv  #Assicurati che questo percorso sia corretto
import random

#Crea l'ambiente FlappyBird
env = FlappyBirdEnv()
done = False
#initilize
obs = env.reset()
#Ciclo di gioco con azioni casuali
while not done:
    #Seleziona un'azione casuale
    action = random.choice([0, 1])
    print(action)
    #Esegui l'azione e ottieni il nuovo stato, la ricompensa, se il gioco è finito
    obs, reward, doned, _ = env.step(action)
    
    #Renderizza l'ambiente
    env.render()

# Chiudi l'ambiente
env.close()