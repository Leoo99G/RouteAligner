import json
import pandas as pd
from Datasets_Generation.json_to_matrix import dict_to_matrix
from datasketch import MinHash, MinHashLSH
from similarity import similarity_sr_ar


# In this script I will, for every driver:
# - collect all the actual routes carried out by that driver (from the actual.json file)
# - convert that json file, the standard.json file and the recStandard.json files to dataframes
#   (matrix representation of sets) and merge them
# - use minhashing on the dataframe to find the standard routes that, on average, have a higher
#   Jaccard similarity with the actual routes of the current driver (get the first 20 standard
#   routes)
# - Find, using my measure of similarity (instead of the Jaccard similarity), the 5 standard
#   routes that are more similar, on average, to the actual routes of the current driver.




def get_sroute(sroute_id, original_sroutes, updated_sroutes) -> dict:
    """
    Given a standard route id, return the corresponding standard route: it can
    be from the original standard routes (if the id starts with "s", e.g. "s5")
    or from the updated/recommended standard routes (if the id starts with "R",
    e.g. "Rs3").

    :param sroute_id: standard route id (string)
    :param original_sroutes: original standard routes (from the file standard.json)
    :param updated_sroutes: updated/recommended standard routes (from the file recStandard.json)
    :return: standard route that matches the input id (there is one and one only such route)
    """
    if sroute_id[0] == 's':
        for sroute in original_sroutes:
            if sroute['id'] == sroute_id:
                return sroute
        print(f"Warning: Standard route with ID {sroute_id} not found in original_sroutes.")
    else:
        for sroute in updated_sroutes:
            if sroute['id'] == sroute_id:
                return sroute
        print(f"Warning: Standard route with ID {sroute_id} not found in updated_sroutes.")


def five_best_routes(dataset_number: int, include_similarities: bool = False):
    """
    :param dataset_number: number of the actual.json file to be used (for example, if you
    want to use the file actual7.json then set dataset_number = 7)
    :param include_similarities: if True, the five best routes for each driver are returned,
    together with their average similarities with the actual routes implemented by the drivers
    :return: a list of dictionaries (one dictionary for each driver). Each dictionary contains
    the driver id and the five best routes for that driver.
    """

    # Import the actual.json file
    with open('../data/actual' + str(dataset_number) + '.json', 'r') as file:
        actual_routes = json.load(file)

    # Import the standard.json file
    with open('../data/standard' + str(dataset_number) + '.json', 'r') as file:
        standard_routes = json.load(file)

    # Import the recStandard.json file
    with open('../results/recStandard' + str(dataset_number) + '.json', 'r') as file:
        updated_standard_routes = json.load(file)
    # Modify the route id for the updated standard routes by adding an "R" in front
    # of the id to distinguish them from the original standard routes
    for route in updated_standard_routes:
        route['id'] = 'R' + route['id']

    # Extract all drivers (from the actual routes) so that we can iterate over them
    drivers = set(route['driver'] for route in actual_routes)

    five_best_routes_list = []

    for k, driver in enumerate(drivers):

        # print(f'Driver {driver} ({k+1}/{len(drivers)}): ')
        # print()

        current_driver_routes = {'driver': str(driver),
                                 'routes': None}

        # Extract all actual routes carried out by the current driver
        routes = [route for route in actual_routes if route['driver'] == driver]

        # Create a unique json file (Python list of dictionaries)
        allroutes = routes + standard_routes + updated_standard_routes

        # Convert each route to a set and create its matrix representation
        # (it is actually a pandas dataframe in which every row is a route)
        # to apply minhashing and estimate the Jaccard similarity between the
        # actual routes carried out by the current driver and the pool of
        # standard routes
        df = dict_to_matrix(allroutes)

        # Function to create a MinHash for a set
        # Number of hash functions to be used
        nperm = 100

        def create_minhash(s):
            minhash = MinHash(num_perm=nperm)
            for element in s:
                minhash.update(str(element).encode('utf-8'))
            return minhash

        # Add a MinHash column to the DataFrame
        df['MinHash'] = df['Set'].apply(create_minhash)

        # Create a MinHashLSH index
        lsh = MinHashLSH(threshold=0.1, num_perm=nperm)

        # Indexing MinHashes
        for index, row in df.iterrows():
            lsh.insert(str(row['Set']), row['MinHash'])

        # Estimate Jaccard Similarity between rows
        result = pd.DataFrame(index=df['Set'], columns=df['Set'])

        for i, row1 in df.iterrows():
            for j, row2 in df.iterrows():
                if i != j:
                    jaccard_similarity = row1['MinHash'].jaccard(row2['MinHash'])
                    result.at[row1['Set'], row2['Set']] = jaccard_similarity

        # Display the result
        # print("Jaccard Similarity Matrix computed.")
        # print('Estimated Jaccard similarities for driver ' + str(driver) + ':')
        # print(result)

        # Convert index to strings and filter rows starting with 'a'
        a_rows = result.index[result.index.astype(str).str.startswith('a')]

        # Filter columns starting with 's' or 'Rs'
        selected_columns = result.filter(regex='^s|^Rs', axis=1)

        # Calculate mean for selected columns over rows that start with 'a'
        means_series = selected_columns.loc[a_rows].mean()

        # Convert the Series to a DataFrame
        means_df = pd.DataFrame(means_series, columns=['Mean'])

        # Sort the DataFrame based on the 'Mean' column in descending order
        n = 15  # First n rows to keep
        means_df = means_df.sort_values(by='Mean', ascending=False).head(n)

        # Display the top n values
        # print(means_df)

        # List of selected standard routes ids
        selected_sroutes = means_df.index.astype(str).tolist()

        # Initialize a dictionary to store the true similarities
        true_similarities_dict = {route_id: None for route_id in selected_sroutes}

        for candidate_s_route_id in selected_sroutes:

            # Extract the standard route with id candidate_s_route_id
            candidate_s_route = get_sroute(candidate_s_route_id, standard_routes, updated_standard_routes)

            sim_current_sroute = []
            for actual_route in routes:
                sim_current_sroute.append(round(similarity_sr_ar(candidate_s_route, actual_route, w1=0.5), 2))

            # Set the value in the corresponding key
            true_similarities_dict[candidate_s_route_id] = round(sum(sim_current_sroute) / len(sim_current_sroute), 2)

        # print('True similarities of the selected standard routes: ')
        # print(true_similarities_dict)
        # print()

        # Sort the dictionary based on values in descending order
        sorted_dict = dict(sorted(true_similarities_dict.items(), key=lambda item: item[1], reverse=True))

        # Keep only the first k items
        k = 5
        top_k_dict = dict(list(sorted_dict.items())[:k])

        if include_similarities:
            current_driver_routes['routes'] = top_k_dict
        else:
            current_driver_routes['routes'] = list(top_k_dict.keys())

        five_best_routes_list.append(current_driver_routes)

        # print(f'Top 5 standard routes for current driver (driver {driver})')
        # print(top_k_dict)

    return five_best_routes_list


# # Test
# a = five_best_routes(dataset_number=8, include_similarities=True)
# print(a)
