import re
import sys
import os
import time

from src.ideal_routes import ideal_routes_by_driver
from src.updated_route_to_json import *
from src.update_routes import recommend_routes
from Datasets_Generation.Dict_to_dataframe import actual_to_dataframe, standard_to_dataframe
from src.top5routes import five_best_routes


def main(input_filename):

    t1 = time.time()  # Record the start time

    # Ensure the "results" directory exists, create it if not
    os.makedirs('../results', exist_ok=True)

    # Check whether the input file name is in the correct format
    pattern = re.compile(r'^actual\d+\.json$')
    match = bool(pattern.match(input_filename))

    if match:
        # Look for the number in the file name
        number = int(re.search(r'\d+', input_filename).group())
    else:
        print('Error: Invalid JSON file name for actual routes.')
        print('The file name should be in the format "actual{number}.json", e.g., actual1.json')
        sys.exit(1)  # Exit with an error code

    # Load the input file actual.json
    with open(f'../data/actual{number}.json', 'r') as file:
        actual_routes = json.load(file)

    # Load the standard.json file
    with open(f'../data/standard{number}.json', 'r') as file:
        st_routes = json.load(file)

    # Turn the input JSON file of actual routes into a Pandas dataframe
    print(f'Converting the file actual{number}.json file to dataframe...')
    actual_routes_df = actual_to_dataframe(actual_routes)

    # Turn the standard routes to Pandas dataframe
    print(f'Converting the file standard{number}.json file to dataframe...')
    st_routes_df = standard_to_dataframe(st_routes)

    t2 = time.time()
    print(f'Standard and actual routes converted to Pandas dataframe. Time taken: {t2 - t1:.2f} seconds.')

    # 1) recStandard.json

    new_st_routes, upd_merch = recommend_routes(actual_routes_df, st_routes_df, freq=0.02)

    # Write the new standard routes into a JSON string
    output_data = generate_json(new_st_routes, upd_merch)

    # Write output json file in the directory "data"
    with open(f'../results/recStandard{number}.json', "w") as output_file:
        output_file.write(output_data)

    t3 = time.time()
    print(f'(1/3) File recStandard{number}.json written in the directory "results". Time taken: {t3 - t2:.2f} seconds.')

    # 2) driver.json file

    # Load the recStandard.json file just created
    with open(f'../results/recStandard{number}.json', 'r') as file:
        upd_st_routes = json.load(file)

    drivers_best_routes = five_best_routes(actual_routes, st_routes, upd_st_routes, n=20)

    # Write output json file in the directory results
    with open(f'../results/driver{number}.json', 'w') as json_file:
        json.dump(drivers_best_routes, json_file, indent=4)
    t4 = time.time()
    print(f'(2/3) File driver{number}.json written in the directory "results". Time taken: {t4 - t3:.2f} seconds.')

    # 3) perfectRoute.json

    # Get ideal routes and merchandise by driver
    ideal_routes, ideal_merchandise = ideal_routes_by_driver(actual_routes_df)

    # Compose a json string
    perfectroute_json_string = generate_json_ideal_route_by_driver(ideal_routes, ideal_merchandise)

    # Write output json file in the directory "data"
    with open(f'../results/perfectRoute{number}.json', "w") as output_file:
        output_file.write(perfectroute_json_string)

    t5 = time.time()
    print(f'(3/3) File perfectRoute{number}.json written in the directory "results".'
          f' Time taken: {t5 - t4:.2f} seconds.')

    print(f'Total execution time: {t5 - t1:.2f} seconds.')


if __name__ == "__main__":
    main(input_filename='actual3.json')
