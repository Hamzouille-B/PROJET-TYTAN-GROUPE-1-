import json
import csv
import os
from glob import glob
from datetime import datetime

def jsons_to_csv(directory, output_csv):
    # Ouvre le fichier CSV et écrit l'en-tête
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['CPU', 'RAM', 'DISQUE', 'DATE']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Liste pour suivre les fichiers JSON à supprimer après leur traitement
        json_files_to_delete = []

        # Parcours tous les fichiers JSON dans le dossier spécifié
        for json_file in glob(os.path.join(directory, '*.json')):
            with open(json_file, 'r') as jfile:
                # Charge les données JSON
                data = json.load(jfile)

                # Vérifie que toutes les clés nécessaires sont présentes
                if all(key in data for key in fieldnames):
                    # Écrivez les données dans le fichier CSV
                    writer.writerow({field: data.get(field) for field in fieldnames})
                    # Ajoute le fichier à la liste des fichiers à supprimer
                    json_files_to_delete.append(json_file)
                else:
                    print(f"Le fichier {json_file} est incomplet et a été ignoré.")

        # Supprime les fichiers JSON traités
        for json_file in json_files_to_delete:
            os.remove(json_file)

# Dossiers contenant les fichiers JSON
directories = ['/home/hamza/analyse_serveur_premier', '/home/hamza/analyse_serveur_second']
date_str = datetime.now().strftime("%Y%m%d")  # Format de la date pour le nom de fichier

# Boucle sur chaque dossier et crée un fichier CSV correspondant
for directory in directories:
    dir_name = os.path.basename(directory)  # Extrait le nom du dossier
    output_csv = f'{dir_name}_{date_str}.csv'  # Nomme le fichier CSV avec le nom du dossier et la date
    jsons_to_csv(directory, os.path.join(directory, output_csv))
    print(f'Les fichiers JSON du dossier "{directory}" ont été convertis en "{output_csv}"')
