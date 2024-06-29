from matplotlib import pyplot as plt
from math import sqrt
from similarity import jaccard_sim_dict
import json


# Iterate over the drivers and for each driver
# compare its ideal route with all the actual
# routes that driver has performed. Ideal routes will be
# considered as standard routes.

dataset_number = 3

# Load actual routes
with open(f'../data/actual{dataset_number}.json', 'r') as file:
    actual_routes = json.load(file)

# Load ideal routes of drivers
with open(f'../Results/perfectRoute{dataset_number}.json', 'r') as file:
    ideal_routes_list = json.load(file)



# I write a modified version of the similarity function just because the format of the
# ideal route in the perfectRoute.jso file differs (ideal routes are lists instead of dictionaries).
# The way it computes similarity is exactly the same.
def similarity_sr_ar2(sroute: list, aroute: dict, w1: float = 0.5) -> float:
    """
    This function computes the similarity between a standard route and an actual route.
    :param sroute: standard route given as a Python list of dictionaries
    :param aroute: actual route given as a Python dictionary
    :param w1: weight for the 1st similarity (Jaccard similarity for the visited cities)
               (1-w1) is the weight for the 2nd similarity (J_merch)
    :return: similarity value (float) between 0 and 1
    """

    # Compute J_cities

    standard_visited_cities = set(trip['from'] for trip in sroute)
    standard_visited_cities.update(trip['to'] for trip in sroute)

    actual_visited_cities = set(trip['from'] for trip in aroute['route'])
    actual_visited_cities.update(trip['to'] for trip in aroute['route'])

    intersection = len(standard_visited_cities.intersection(actual_visited_cities))
    union = len(standard_visited_cities.union(actual_visited_cities))

    j_cities = intersection / union if union else 0

    # Compute J_merch

    sim_scores_merch = []
    ac_dest_cities = [trip['to'] for trip in aroute['route']]

    for st_trip in sroute:
        if st_trip['to'] in ac_dest_cities:
            # I know that the dest city of the current st trip is a dest
            # city of some actual trip. I have to find all the ac trips
            # with this destination and append the max similarity
            max_sim = 0
            for ac_trip in aroute['route']:
                if ac_trip['to'] == st_trip['to'] and \
                        jaccard_sim_dict(st_trip['merchandise'], ac_trip['merchandise']) > max_sim:
                    max_sim = jaccard_sim_dict(st_trip['merchandise'], ac_trip['merchandise'])
            sim_scores_merch.append(max_sim)
        else:
            sim_scores_merch.append(0)

    j_merch = sum(sim_scores_merch) / len(sim_scores_merch)

    return w1 * j_cities + (1-w1) * j_merch


# Compute driver's average similarity from their ideal route
sims = []
for driver_info in ideal_routes_list:
    curr_driver_id = driver_info['driver']  # driver id
    curr_driver_ideal_route = driver_info['route']  # ideal route (list of dictionaries)
    curr_driver_ac_routes = [route for route in actual_routes if route['driver'] == curr_driver_id]
    sims = []
    for aroute in curr_driver_ac_routes:
        sims.append(similarity_sr_ar2(curr_driver_ideal_route, aroute))
    sims.append(sum(sims)/len(sims))

# Mean similarity for each driver
# print([round(x, 6) for x in sims])
print(sims)

avg_sim = sum(sims) / len(sims)
print('Mean: ', round(avg_sim, 3))

st_dev = sqrt(1/(len(sims)-1) * sum([(x-avg_sim)**2 for x in sims]))
print('Standand deviation: ', round(st_dev, 3))


# Number of