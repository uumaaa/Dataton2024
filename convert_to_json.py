import json
import pandas as pd

df = pd.read_csv("aspirantes.csv")
map = {}
for index, row in df.iterrows():
    if (row['name'] in map):
        map[row['name']]['cargoAlQueAspira'].append(row['position'])
    else:
        map[row['name']] = {
        'folio': row['folio'],
        'fechaInscripcion': row['date'],
        'nombreCompleto': row['name'],
        'cargoAlQueAspira': [row['position']]
        }

list_of_participants = []
for key, value in map.items():
    list_of_participants.append(value)

data = json.dumps(list_of_participants, sort_keys=True, indent=4)
with open("aspirantes.json", "w") as outfile:
    outfile.write(data)
