from flask import Flask, request, jsonify
from datetime import datetime
import os
import json

app = Flask(__name__)

@app.route('/recevoir-json', methods=['POST'])
def receive_data():
    data = request.get_json()
    required_keys = ['CPU', 'RAM', 'DISQUE', 'DATE']

    if not data:
        return jsonify({"Erreur": "Pas de données"}), 400

    # Vérifie que toutes les clés nécessaires sont présentes
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        # Renvoie un message d'erreur si des clés sont manquantes
        return jsonify({"Erreur": f"Il manque les données pour les clés suivantes: {', '.join(missing_keys)}"}), 400

    # Récupère l'adresse IP de la machine émettrice
    ip_address = request.remote_addr

    # Sélectionne le dossier de destination basé sur l'adresse IP
    if ip_address == '192.168.1.151':
        directory = 'analyse_serveur_premier'
    elif ip_address == '192.168.1.152':
        directory = 'analyse_serveur_second'
    else:
        return jsonify({"Erreur": "Adresse IP non reconnue"}), 400

    # Crée le dossier s'il n'existe pas
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Formatte le nom de fichier
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{directory}/{ip_address}_{timestamp}.json"

    # Écrit les données dans un fichier JSON
    with open(filename, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)

    print(f"Data saved to {filename}")
    return jsonify({"message": "Données reçues et enregistrées"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
