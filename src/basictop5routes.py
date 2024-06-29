from similarity import similarity_sr_ar

# This file is used to test Task 2

# In this script I will,
# for every driver:
# - collect all the actual routes carried out by that driver (from the actual.json file)
# For each standard route (id) (that has been implemented by the current driver):
# - get all the actual routes of the current driver that implement the current standard route
#   (In case there are more related actual routes, average the similarities.)
# compute the true average similarity to the related actual routes.
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


def basic_five_best_routes(actual_routes, standard_routes, updated_standard_routes,
                           include_similarities: bool = False):
    """
    :param include_similarities: if True, the five best routes for each driver are returned,
    together with their average similarities with the actual routes implemented by the drivers
    :return: a list of dictionaries (one dictionary for each driver). Each dictionary contains
    the driver id and the five best routes for that driver.
    """

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

        current_driver_5routes = {'driver': str(driver),
                                  'routes': None}

        # Extract all actual routes carried out by the current driver
        current_driver_aroutes = [route for route in actual_routes if route['driver'] == driver]
        # Extract the SR ids of the routes implemented by the current driver
        curr_driver_sroutes_id = set(route['sroute'] for route in current_driver_aroutes)

        true_similarities_dict = {}
        for sroute_id in curr_driver_sroutes_id:
            # Get the original standard route with the current id
            orig_sroute = get_sroute(sroute_id, standard_routes, updated_standard_routes)
            # Get the corresponding SR from the updated ones
            upd_sroute = get_sroute('R' + sroute_id, standard_routes, updated_standard_routes)

            # Get the actual routes (of the current driver) that implement the current SR
            related_aroutes = [route for route in current_driver_aroutes if route['sroute'] == sroute_id]

            similarities_with_orig = []  # list to store the similarities of the ARs to the original SR
            similarities_with_upd = []  # list to store the similarities of the ARs to the updated SR

            for aroute in related_aroutes:
                # Compare the current (original) SR to AR
                similarities_with_orig.append(similarity_sr_ar(orig_sroute, aroute))
                # Compare the current (updated) SR to AR
                similarities_with_upd.append(similarity_sr_ar(upd_sroute, aroute))

            true_similarities_dict[sroute_id] = sum(similarities_with_orig) / len(similarities_with_orig)
            true_similarities_dict['R' + sroute_id] = sum(similarities_with_upd) / len(similarities_with_upd)

        # Sort the dictionary based on values in descending order
        true_similarities_dict = dict(sorted(true_similarities_dict.items(),
                                             key=lambda item: item[1],
                                             reverse=True))

        # print('True similarities of the standard routes: ')
        # print(true_similarities_dict)
        # print()

        # Keep only the first
        top_k_dict = dict(list(true_similarities_dict.items())[:5])

        if include_similarities:
            current_driver_5routes['routes'] = top_k_dict
        else:
            current_driver_5routes['routes'] = list(top_k_dict.keys())

        five_best_routes_list.append(current_driver_5routes)

        # print(f'Top 5 standard routes for driver {driver} computed ({k+1}/{len(drivers)}).')
        # print(top_k_dict)
        # print()

    return five_best_routes_list
