import pandas as pd
import matplotlib.pyplot as plt

# Percorso del file monitor.csv
log_path = "C:/Users/madda/Desktop/FlappyBirdAI/Logs/monitor.csv"


# Leggi i dati dal file monitor.csv
try:
    data = pd.read_csv(log_path, skiprows=1)  # Salta la prima riga di commento
    print("Dati caricati con successo.")
except FileNotFoundError:
    print(f"File {log_path} non trovato. Assicurati di aver avvolto l'ambiente con Monitor.")
    exit()

# Mostra alcune righe per verificare il contenuto
print(data.head())

# Estrai le colonne rilevanti
episodes = data['l'].cumsum()  # Lunghezza cumulativa degli episodi (timesteps)
rewards = data['r']  # Ricompense per episodio

# Creazione del grafico
plt.figure(figsize=(10, 6))
plt.plot(episodes, rewards, label='Ricompensa per episodio', alpha=0.8)
plt.xlabel("Timesteps")
plt.ylabel("Ricompensa")
plt.title("Progressi dell'agente durante l'addestramento")
plt.legend()
plt.grid()
plt.show()