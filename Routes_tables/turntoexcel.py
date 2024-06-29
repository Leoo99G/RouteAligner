from Datasets_Generation.Dict_to_dataframe import actual_to_dataframe, standard_to_dataframe
import json


with open('../data/actual2.json', 'r') as file:
    actual_routes = json.load(file)
df = actual_to_dataframe(actual_routes)
df.to_csv('actual_routes_table_2.csv', index=False)

with open('../data/standard2.json', 'r') as file:
    original_standard_routes = json.load(file)
df = standard_to_dataframe(original_standard_routes)
df.to_csv('standard_routes_table_2.csv', index=False)

with open('../results/recStandard2.json', 'r') as file:
    updated_standard_routes = json.load(file)
df = standard_to_dataframe(updated_standard_routes)
df.to_csv('updated_standard_routes_table_2.csv', index=False)

