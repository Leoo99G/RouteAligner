from Datasets_Generation.json_to_matrix import dict_to_set
from datasketch import MinHash
from similarity import similarity_sr_ar


# In this script I will,
# for every driver:
# - collect all the actual routes carried out by that driver (from the actual.json file)
# For each standard route (id) (that has been implemented by the current driver):
# - get all the actual routes of the current driver that implement the current standard route
# - use minhashing to estimate the Jaccard similarity between the current SR and its related ARs
#   (after converting the two routes to sets).
#   (In case there are more related actual routes, average the similarities.)
# - Add the standard route id to a dictionary and set its value as the average similarity computed.
# - Keep the N (= 20) standard routes with the highest similarity scores.
# - On the N selected standard routes, compute the true average similarity to the related actual routes.
# - Keep the standard routes with the 5 highest similarities.


# The output should be in the following format:
#
# [
# 	{driver: "C", routes: ["s10", "s20", "s2", "s6", "s10"]},
# 	{driver: "A", routes: ["s1", "s2", "s22", "s61", "s102"]},
# …
# ]

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


def estimate_jaccard(set1: set, set2: set, nperm: int = 200) -> float:
    m1, m2 = MinHash(num_perm=nperm), MinHash(num_perm=nperm)
    for d in set1:
        m1.update(d.encode('utf8'))
    for d in set2:
        m2.update(d.encode('utf8'))
    return m1.jaccard(m2)


def five_best_routes(actual_routes: list, standard_routes: list, updated_standard_routes: list,
                     n: int = 20, include_similarities: bool = False) -> list:
    """
    :param actual_routes: list of actual routes
    :param standard_routes: list of original standard routes
    :param updated_standard_routes: list of recommended standard routes
    :param include_similarities: if True, the five best routes for each driver are returned,
    together with their average similarities with the actual routes implemented by the drivers
    :param n: number of SRs to select before computing the true average similarities
    :return: a list of dictionaries (one dictionary for each driver). Each dictionary contains
    the driver id and the five best routes for that driver.
    """

    for route in updated_standard_routes:
        route['id'] = 'R' + route['id']

    # Extract all drivers (from the actual routes) so that we can iterate over them
    drivers = set(route['driver'] for route in actual_routes)

    five_best_routes_list = []

    for k, driver in enumerate(drivers):

        # print(f'Driver {driver} ({k+1}/{len(drivers)}): ')
        # print()

        current_driver_5routes = {'driver': str(driver),
                                  'routes': None}

        # Extract all actual routes carried out by the current driver
        current_driver_routes = [route for route in actual_routes if route['driver'] == driver]
        # Extract the SR ids of the routes implemented by the current driver
        curr_driver_sroutes_id = set(route['sroute'] for route in current_driver_routes)

        # Create a dictionary of SRs where to store the average estimated
        # similarities for the current driver
        sroute_dict = {}

        # Iterate over the SRs
        for route_id in curr_driver_sroutes_id:
            # Get the original standard route with the current id
            orig_sroute = get_sroute(route_id, standard_routes, updated_standard_routes)
            # Get the corresponding SR from the updated ones
            upd_sroute = get_sroute('R' + route_id, standard_routes, updated_standard_routes)

            # Get the actual routes (of the current driver) that implement the current SR
            related_aroutes = [route for route in current_driver_routes if route['sroute'] == route_id]

            if related_aroutes:  # Check if the driver implemented the current SR
                similarities_with_orig = []  # list to store the similarities of the ARs to the original SR
                similarities_with_upd = []  # list to store the similarities of the ARs to the updated SR

                for aroute in related_aroutes:
                    # Compare the current (original) SR to AR
                    osr = dict_to_set(orig_sroute)
                    ar = dict_to_set(aroute)
                    similarities_with_orig.append(estimate_jaccard(osr, ar))

                    # Compare the current (updated) SR to AR
                    usr = dict_to_set(upd_sroute)
                    similarities_with_upd.append(estimate_jaccard(usr, ar))

                sroute_dict[route_id] = sum(similarities_with_orig) / len(similarities_with_orig)
                sroute_dict['R' + route_id] = sum(similarities_with_upd) / len(similarities_with_upd)

            else:
                sroute_dict[route_id] = -1
                sroute_dict['R' + route_id] = -1
                # Flags to indicate that SR was never implemented by the current driver
                # When I sort the dictionary, those SR will always be in the last places

        # Sort the dictionary by values in descending order
        sroute_dict = dict(sorted(sroute_dict.items(), key=lambda item: item[1], reverse=True))
        # print(f'Estimated Jaccard similarities for driver {driver}:')
        # print(sroute_dict)

        # Extract the first n keys
        selected_sroutes_id = list(sroute_dict.keys())[:n]

        # Now in the dictionary selected_sroutes_id we have the ids of the
        # standard routes with the n highest estimated jaccard similarities
        # to the AR s of the current driver. Among these n SRs, we need to
        # select only 5, after computing the average true similarities.

        # Initialize a dictionary to store the true similarities
        true_similarities_dict = {}

        for candidate_sroute_id in selected_sroutes_id:
            # Extract the standard route with id candidate_s_route_id
            candidate_sroute = get_sroute(candidate_sroute_id, standard_routes, updated_standard_routes)

            if candidate_sroute_id[0] == 'R':
                related_aroutes = [route for route in current_driver_routes if route['sroute'] == candidate_sroute_id[1:]]
            else:
                related_aroutes = [route for route in current_driver_routes if route['sroute'] == candidate_sroute_id]

            # Check if there are any related actual routes before going on
            if related_aroutes:
                true_sims_current_sroute = []
                for actual_route in related_aroutes:
                    true_sims_current_sroute.append(similarity_sr_ar(candidate_sroute, actual_route, w1=0.5))

                # Set the value in the corresponding key
                true_similarities_dict[candidate_sroute_id] = sum(true_sims_current_sroute) / len(true_sims_current_sroute)
            else:
                true_similarities_dict[candidate_sroute_id] = -1
                # Flag to indicate the current driver never implemented the current SR

        # Sort the dictionary based on values in descending order
        true_similarities_dict = dict(sorted(true_similarities_dict.items(),
                                             key=lambda item: item[1],
                                             reverse=True))

        # print('True similarities of the selected standard routes: ')
        # print(true_similarities_dict)
        # print()

        # Keep only the first
        top_k_dict = dict(list(true_similarities_dict.items())[:5])

        if include_similarities:
            current_driver_5routes['routes'] = top_k_dict
        else:
            current_driver_5routes['routes'] = list(top_k_dict.keys())

        five_best_routes_list.append(current_driver_5routes)

        print(f'Top 5 standard routes for driver {driver} computed ({k+1}/{len(drivers)}).')
        # print(top_k_dict)
        # print()

    return five_best_routes_list
