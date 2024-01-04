import psutil
import requests
from datetime import datetime

def collect_data():
    # Collecting system metrics
    metrics = {
        "CPU": psutil.cpu_percent(interval=1),
        "RAM": psutil.virtual_memory().percent,
        "DISQUE": psutil.disk_usage('/').percent,  # Mis à jour pour correspondre à la clé attendue
        "DATE": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Mis à jour pour correspondre à la clé attendue
    }
    return metrics

def send_data_to_api(data):
    url = 'http://192.168.1.150:5000/recevoir-json'  # Assurez-vous que l'adresse IP et le port sont corrects
    response = requests.post(url, json=data)
    return response

if __name__ == "__main__":
    data = collect_data()
    response = send_data_to_api(data)
    if response.status_code == 200:
        print("Les données ont été envoyées avec succès.")
    else:
        print(f"Échec de l'envoi des données : {response.status_code} - {response.text}")