import json
import pandas as pd
import numpy as np
import os


def verify_keys(dictionary, keys):
    return all(key in dictionary for key in keys)
def create_dataframe(path):
    total_df = pd.DataFrame()
    folders = os.listdir(path)
    for folder in folders:
        files = os.listdir(os.path.join(path, folder))
        for file in files:
            if file.endswith(".json"):
                df = pd.read_json(os.path.join(path,folder,file))
                total_df = pd.concat([total_df,df])
    return  total_df

total_df = create_dataframe("s3s")
sancionados = total_df['servidorPublicoSancionado'].to_numpy()
map = {}
for sancionado in sancionados:
    if(verify_keys(sancionado,['nombres','primerApellido','segundoApellido'])):
        nombreCompleto = sancionado['nombres'] + " " + sancionado['primerApellido'] + " " + sancionado['segundoApellido']
        map[nombreCompleto] = 1

df_2 = pd.read_json("aspirantes.json")
for index,row in df_2.iterrows():
        if(row['nombreCompleto'] in map):
            print(row['nombreCompleto'])



