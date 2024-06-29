
# This file makes the following things:

# 1. Generate standard and actual routes in the format of Python lists (function generate_random_routes)
# 2. Turn the routes into json files (and saves them in the directory "data") (function write_to_json)
# 3. Turns the json files created above into csv (or Pandas dataframes)


import generate_random_routes
from routes_to_json import write_to_json
import os
import json
from Dict_to_dataframe import standard_to_dataframe, actual_to_dataframe

from config_dataset_4 import(
    cities,
    merchandise_types,
    drivers,
    dataset_number,
    NUM_SROUTES,
    MINNCITIES,
    MAXNCITIES,
    MAXNUMITEMS,
    MAXQUANTITY,
    AVERAGE_NUM_ACTUAL,
    ST_DEV_ACTUAL,
    P_CITIES_REPLACE,
    P_MOD,
    P_QUANT_CHANGE,
    P_ADD,
    P_REMOVE,
    RANDOM_SEEDS,
    USE_REPLACEMENT_SET,
    cities_for_replacement
)

# Generate standard and actual routes (in the form of Python lists/dictionaries)
standard_routes, actual_routes = generate_random_routes.generate_routes(cities=cities,
                                                                        merchandise_types=merchandise_types,
                                                                        drivers=drivers,
                                                                        num_sroutes=NUM_SROUTES,
                                                                        minncities=MINNCITIES,
                                                                        maxncities=MAXNCITIES,
                                                                        maxnumitems=MAXNUMITEMS,
                                                                        maxquantity=MAXQUANTITY,
                                                                        average_num_actual=AVERAGE_NUM_ACTUAL,
                                                                        st_dev_actual=ST_DEV_ACTUAL,
                                                                        p_cities_replace=P_CITIES_REPLACE,
                                                                        p_mod=P_MOD,
                                                                        p_quant_change=P_QUANT_CHANGE,
                                                                        p_add=P_ADD,
                                                                        p_remove=P_REMOVE,
                                                                        rand_seeds=RANDOM_SEEDS,
                                                                        use_replacement_set=USE_REPLACEMENT_SET,
                                                                        cities_for_replacement=cities_for_replacement)


# Turn standard_routes and actual_routes lists to json and save them in the directory "data".
external_directory = 'data'
standard_name = f"standard{dataset_number}.json"  # Name to give to the json file for the standard routes
actual_name = f"actual{dataset_number}.json"  # Name to give to the json file for the actual routes
write_to_json(standard_routes, actual_routes, standard_name, actual_name, external_directory)


# Turn the json files into csv (or Pandas dataframes) and save it in the directory "Routes_tables"

# Name of the json file containing the standard routes
standard_json_file_name = standard_name
# Name to save the csv file for the standard routes
standard_csv = f"standard_routes_table_{dataset_number}.csv"

# Name of the json file containing the actual routes
actual_json_file_name = actual_name
# Name to save the csv file for the actual routes
actual_csv = f"actual_routes_table_{dataset_number}.csv"

# Specify the directory names
output_directory = 'Routes_tables'

# Get the absolute path to the script directory
script_path = os.path.abspath(os.path.dirname(__file__))
# Construct the absolute path to the external directory
external_path = os.path.join(script_path, '..', external_directory)
# Construct the absolute path to the output directory
output_path = os.path.join(script_path, '..', output_directory)

# STANDARD ROUTES TO DATAFRAME/CSV

# Construct the absolute path to the standard.json file
standard_json_path = os.path.join(external_path, standard_json_file_name)

# Check if the file exists before attempting to open it
if os.path.exists(standard_json_path):
    # Open the JSON file
    with open(standard_json_path, 'r') as file:
        data = json.load(file)

        combined_route_df = standard_to_dataframe(data)

# Save the dataframe as a CSV file

    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Save the Pandas DataFrame as a CSV file
    csv_file_path_standard = os.path.join(output_path, standard_csv)
    combined_route_df.to_csv(csv_file_path_standard, index=False)

    print(f"CSV file saved at: {os.path.abspath(csv_file_path_standard)}")
else:
    print(f"The file {standard_json_path} does not exist.")


# ACTUAL ROUTES TO DATAFRAME/CSV

# Construct the absolute path to the standard.json file
actual_json_path = os.path.join(external_path, actual_json_file_name)

# Check if the file exists before attempting to open it
if os.path.exists(actual_json_path):
    # Open the JSON file
    with open(actual_json_path, 'r') as file:
        data = json.load(file)

        combined_route_df = actual_to_dataframe(data)

    # Save the Pandas DataFrame as a CSV file
    csv_file_path_actual = os.path.join(output_path, actual_csv)
    combined_route_df.to_csv(csv_file_path_actual, index=False)

    print(f"CSV file saved at: {os.path.abspath(csv_file_path_actual)}")
else:
    print(f"The file {actual_json_path} does not exist.")
