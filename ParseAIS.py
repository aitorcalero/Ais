import json
import csv
import os

directory = os.getcwd()
i = 0
csv_columns = ['ID','Name','MMSI','Lon','Lat','ship_type','flag','speed','heading','course']
csv_data = []

for filename in os.listdir(directory):
    if filename.endswith('.json'):
        with open(filename) as json_file:  
            data = json.load(json_file)
            for p in data['data']:
                last_known_position = p['last_known_position']
                coords = last_known_position['geometry']['coordinates']
                row_data = [str(i),p['name'],str(p['mmsi']), \
                    str(coords[0]),str(coords[1]), \
                    p['ship_type'],p['flag'],last_known_position['speed'], \
                    last_known_position['heading'],last_known_position['course']]
                csv_data.append(row_data)
                i +=1

# create de AIS CSV file

csv_file = "Ais.csv"

try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_columns)
        for data in csv_data:
            if any(data):
                writer.writerow(data)
except IOError:
    print("I/O error") 