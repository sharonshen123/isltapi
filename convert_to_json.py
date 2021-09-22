import pandas as pd

cols=["pg","word","definition","sentence","category","sample","synonyms"]
data = pd.read_csv('ISLT_data.csv', sep=',', engine='python', usecols=cols,na_values = [''])
json_data = data.to_json(orient = "records")
print(json_data)