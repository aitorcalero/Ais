import json
import csv

with open('ais.json') as json_file:  
    data = json.load(json_file)
    i = 1
    for p in data['data']:
        print('Name: ' + p['name'])
        print('MMSI: ' + str(p['mmsi']))
        dictPos = p['last_known_position']
        print('Longitude: '+ str(dictPos['geometry']['coordinates'][0]))
        print('Latitude: ' + str(dictPos['geometry']['coordinates'][1]))
        print(str('ID:' + str(i)))
        print(' ')
        i +=1