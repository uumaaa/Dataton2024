import json
import pandas as pd

df = pd.read_csv("aspirantes.csv")
aspirantes = []
for index, row in df.iterrows():
    obj = {
        'folio':row['folio'],
        'fechaInscripcion':row['date'],
        'nombreCompleto':row['name'],
        'cargoAlQueAspira':row['position']
    }
    aspirantes.append(obj)

data = json.dumps(aspirantes, sort_keys=True, indent=4)
with open("aspirantes.json", "w") as outfile:
    outfile.write(data)
