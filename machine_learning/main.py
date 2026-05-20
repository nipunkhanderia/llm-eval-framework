import pandas as pd


melbourne_file_path = r"C:\Users\Nipun\Downloads\llm-eval-frameworkz\machine_learning\train.csv"
melbourne_dataz = pd.read_csv(melbourne_file_path)


# print(melbourne_dataz.describe())


y = melbourne_dataz.SalePrice
print(y)

melbourne_features = ["LotArea","YearBuilt","1stFlrSF","2ndFlrSF","FullBath","BedroomAbvGr","TotRmsAbvGrd"]

X = melbourne_dataz[melbourne_features]
print(X.describe())

