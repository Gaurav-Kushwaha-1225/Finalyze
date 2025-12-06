import pandas as pd
import os
for file in os.listdir('.'):
    if file.endswith('.xlsx'):
        xl = pd.ExcelFile(file)
        for sheet in xl.sheet_names:
            pd.read_excel(file, sheet_name=sheet).to_csv(f"{file}_{sheet}.csv", index=False)
