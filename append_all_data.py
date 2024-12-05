import os
from unidecode import unidecode
import numpy as np
import pandas as pd

def removeprefix_custom(s, prefix):
    if s.startswith(prefix):
        return s[len(prefix):]
    return s


def num_to_word(numero):
    numeros_a_palabra = {
        1: 'Primero', 2: 'Segundo', 3: 'Tercero', 4: 'Cuarto', 5: 'Quinto',
        6: 'Sexto', 7: 'Septimo', 8: 'Octavo', 9: 'Noveno', 10: 'Decimo',
        11: 'Undecimo', 12: 'Duodecimo', 13: 'Decimotercero', 14: 'Decimocuarto',
        15: 'Decimoquinto', 16: 'Decimosexto', 17: 'Decimosetimo', 18: 'Decimoctavo',
        19: 'Decimonoveno', 20: 'Vigesimo', 21: 'Vigesimo primero', 22: 'Vigesimo segundo',
        23: 'Vigesimo tercero', 24: 'Vigesimo cuarto', 25: 'Vigesimo quinto',
        26: 'Vigesimo sexto', 27: 'Vigesimo septimo', 28: 'Vigesimo octavo',
        29: 'Vigesimo noveno', 30: 'Trigésimo'
    }

    return numeros_a_palabra.get(numero, str(numero))

def transform_value(cadena):
    import re
    patron = r'(\d+)°'
    return re.sub(patron, lambda m: num_to_word(int(m.group(1))), cadena)

names = []
folios = []
dates = []
positions = []

files = os.listdir("aspirantes")
for file in files:
    print(file)
    df = pd.read_csv(os.path.join("aspirantes",file), header=None)
    for index, row in df.iterrows():
        num_and_folio = row.iloc[0]
        folio = num_and_folio.split(" ")[2]
        date_and_names = str(row.iloc[1])
        inscription_date = date_and_names.split(" ")[0]
        both_names = removeprefix_custom(date_and_names,inscription_date)
        both_names = both_names.strip()
        p_last_name = row.iloc[2]
        m_last_name = row.iloc[3]
        position = row.iloc[4]
        position = transform_value(position)
        both_names = unidecode("{} {} {}".format(both_names, p_last_name, m_last_name))
        names.append(both_names)
        folios.append(folio)
        dates.append(inscription_date)
        positions.append(unidecode(position))

names = np.array(names)
folios = np.array(folios)
dates = np.array(dates)
positions = np.array(positions)
all_data = np.vstack((folios, dates,names, positions)).T
df = pd.DataFrame(all_data,columns=['folio','date','name','position'])
df.to_csv("aspirantes.csv")
