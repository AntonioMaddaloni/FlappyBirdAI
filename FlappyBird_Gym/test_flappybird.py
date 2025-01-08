import gymnasium as gym
from main import FlappyBirdEnv  #Assicurati che questo percorso sia corretto
import random

#Crea l'ambiente FlappyBird
env = FlappyBirdEnv()
done = False
#Ciclo di gioco con azioni casuali
while not done:
    #Seleziona un'azione casuale
    action = random.choice([0, 1])
    
    #Esegui l'azione e ottieni il nuovo stato, la ricompensa, se il gioco è finito
    env.step(action)
    
    #Renderizza l'ambiente
    env.render()

# Chiudi l'ambiente
env.close()