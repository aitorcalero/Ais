import json
import csv
import os

directory = os.getcwd()
i = 0
csv_columns = ['ID','Name','MMSI','Lon','Lat']
csv_data = []

for filename in os.listdir(directory):
    if filename.endswith('.json'):
        with open(filename) as json_file:  
            data = json.load(json_file)
            for p in data['data']:
                coords = p['last_known_position']['geometry']['coordinates']
                row_data = [str(i),p['name'],str(p['mmsi']),str(coords[0]),str(coords[1])]
                csv_data.append(row_data)
                i +=1

# puedo crear un diccionario sin estructura de árbol y 
# luego convertirlo en CSV directamente con el módulo CSV

csv_file = "Ais.csv"

try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_columns)
        for data in csv_data:
            writer.writerow(data)
except IOError:
    print("I/O error") 