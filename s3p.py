import json
import pandas as pd
import numpy as np
import os

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

total_df = create_dataframe("s3p")
punisheds = total_df['particularSancionado'].to_numpy()
map = {}
for punished in punisheds:
    map[punished['nombreRazonSocial']] = 1

df_2 = pd.read_json("aspirantes.json")
for index,row in df_2.iterrows():
        if(row['nombreCompleto'] in map):
            print(row['nombreCompleto'])



