import pandas as pd


melbourne_file_path = r"C:\Users\Nipun\Downloads\melbourne_data.csv"
melbourne_dataz = pd.read_csv(melbourne_file_path)

print(melbourne_dataz.describe())


