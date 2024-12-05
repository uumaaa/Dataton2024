import pandas as pd


xlsx_file = "aspirantes.xlsx"
excel_data = pd.read_excel(xlsx_file, sheet_name=None)
i = 0
for sheet_name, data in excel_data.items():
    csv_file = f"aspirantes/table_{i}.csv"
    data.to_csv(csv_file, index=False, header=False)
    print(f"Guardado: {csv_file}")
    i += 1
