import csv
from os import write
import json
import yaml
import xml.etree.ElementTree as ET

from seaborn.external.docscrape import header
from ultralytics.utils import yaml_load


class DataFilter:
    def __init__(self):
        self.data =[]

#Fichiers CSV
    def load_csv(self, filepath):
        with open(filepath, 'r') as file :
            reader = csv.DictReader(file)
            self.data = [row for row in reader]
            """
            #sans utiliser Dictrreader on est obligé de suivre cette logique
            reader = csv.reader(file)
            headers = next(reader) #lire la première ligne en tans que header
            self.data = [dict(zip(headers, row)) for row in reader]
            """

    def save_csv(self, filepath):
        if not self.data:
            print("aucune données à sauvgarder")
            return
        with open(filepath, 'w', newline= '') as file:
            writer = csv.DictWriter(file, fieldnames=self.data[0].keys())
            writer.writeheader()
            writer.writerows(self.data)


#Fichiers JSON

    def load_json(self, filepath):
        with open(filepath, 'r') as file:
            self.data = json.load(file)


    def save_json(self, filepath):
        with open(filepath, 'w') as file :
            json.dump(self.data, file, indent=4) #laisser de l'indentation


#Fichier yaml

    def load_yaml(self, filepath):
        with open(filepath, 'r') as file:
           self.data = yaml.safe_load(file) #La fonction yaml.safe_load() du module PyYAML sert à convertir
                                            # le contenu YAML en une structure de données Python
                                            # généralement des dictionnaires ou des listes.

    def save_yaml(self, filepath):
        with open(filepath, 'w') as file:
            yaml.dump(self.data, file)


#Fichiers xml
    def load_xml(self, filepath):
        with open(filepath, 'r') as file:
            tree = ET.parse(filepath) #lit tout le fichier XML pour pouvoir ensuite manipuler ses éléments (retourne un objet ElementTree)
            root = tree.getroot() # récupère l'élément racine du fichier XML
            self.data = [{child.tag: child.text for child in elem} for elem in root] #convertit le XML en Python.

    def save_xml(self, filepath):
        if not self.data:
            return
        root = ET.Element('root')
        for item in self.data:
            item_element = ET.SubElement(root, "item")
            for key, value in item.items():
                child = ET.SubElement(item_element, key)
                child.text = str(value)
            tree = ET.ElementTree(root)
            tree.write(filepath)

    def filter_data(self, key, value):
        return [item for item in self.data if item.get(key) == value]

    def sort_data(self, key):
        self.data.sort(key=lambda x: x.get(key))

    def display_data(self):
        for item in self.data:
            print(item)

# Statistiques des données

    def show_stats(self):
        if not self.data:
            print("Aucune donnée disponible.")
            return
        keys = self.data[0].keys()  # renvoie les cles du premier dictionnaire === cles de tous dictionnaires de la liste
        for key in keys:
            values = [item.get(key) for item in self.data if item.get(key) is not None] #item c'est le dic -> item.get(key) renvoie la la vaeur de la clé
            if all(isinstance(v, (int, float)) for v in values): #vérifier si toutes conditions à l'intérieur sont True : on a des valeurs numérique
                print(f"  Min: {min(values)}")
                print(f"  Max: {max(values)}")
                print(f"  Average: {sum(values) / len(values):.2f}")

            elif all(isinstance(v, bool) for v in values):
                true_count = sum(1 for v in values if v)
                false_count = len(values) - true_count
                total = len(values)
                print(f"  % True: {true_count / total * 100:.2f}%")
                print(f"  % False: {false_count / total * 100:.2f}%")

            elif all(isinstance(v, list) for v in values):
                lengths = [len(v) for v in values]
                print(f"  Min length: {min(lengths)}")
                print(f"  Max length: {max(lengths)}")
                print(f"  Average length: {sum(lengths) / len(lengths):.2f}")