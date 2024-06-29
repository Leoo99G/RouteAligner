######################################################
# This file  contains the function generate_routes
# that generates standard routes and for each
# standard route it creates some actual routes by
# slightly modifying the standard routes
######################################################
import math
import random


def modify_merch(merchandise: dict, merch_types: list, maxquantity: int, p_mod: float, p_quant_change: float):
    """
    The function modify_merch takes a dictionary (keys are types of merchandise and values are
    the quantity of that kind of merchandise) and slightly modifies the merchandise by randomly
    adding, removing items or modifying the quantity.

    :param merchandise: dictionary of merchandise items and quantities in a standard route
    :param merch_types: list of merchandise types where to sample an item to replace an existing one
    :param maxquantity: max modified quantity for an item (when modifying the quantity)
    :param p_mod: probability of modifying an item
    :param p_quant_change: probability of modifying the quantity of an item (among the items that are modified)

    :return: modified version of the dictionary of merchandise items and quantities
    """

    modified_merchandise = {}
    for item, quantity in merchandise.items():
        # Randomly decide to add, remove, or modify quantity of items.
        # The code simulates a 50% chance of modification and, within that 50%,
        # a further 50% chance for adjusting the quantity of the merchandise
        if random.random() < p_mod:  # 50% chance for modification
            if random.random() < p_quant_change:  # 50% chance for quantity change
                quantity += random.randint(-3, 3)  # Adjust quantity randomly
                modified_merchandise[item] = max(1, quantity)
            else:
                # Replace the item with a random one that doesn't exist in the merchandise
                available_items = [m for m in merch_types if m not in merchandise]
                if available_items:  # checks whether the variable available_items contains any elements
                    new_item = random.choice(available_items)
                    modified_merchandise[new_item] = random.randint(1, maxquantity)
        else:
            # Keep the original item and quantity
            modified_merchandise[item] = quantity

    return modified_merchandise


def generate_routes(cities: list,
                    merchandise_types: list,
                    drivers: list,
                    num_sroutes: int,
                    minncities: int,
                    maxncities: int,
                    maxnumitems: int,
                    maxquantity: int,
                    average_num_actual: int,
                    st_dev_actual: int,
                    p_cities_replace: float,
                    p_mod: float,
                    p_quant_change: float,
                    p_add: float,
                    p_remove: float,
                    rand_seeds: list,
                    use_replacement_set: bool,
                    cities_for_replacement: list,
                    ):
    """
    This function generates a list of standard routes and a list of actual routes

    :param cities: list of possible cities for the routes
    :param merchandise_types: list of merchandise types for the routes
    :param drivers: list of drivers for the routes
    :param num_sroutes: number of actual routes to generate
    :param minncities: minimum number of cities to be visited at each trip
    :param maxncities: max number of items to select for each trip
    :param maxnumitems: max number of items to select for each trip
    :param maxquantity: max quantity for each item
    :param average_num_actual: average number of actual routes to create from each standard route
    (sampled from a normal distribution)
    :param st_dev_actual: standard deviation of the number of actual routes to create from each standard route
    :param p_cities_replace: maximum percentage of cities in an actual route to replace
    :param p_mod: parameter to pass to the modify_merch function
    :param p_quant_change: parameter to pass to the modify_merch function
    :param p_add: probability of adding random cities in an actual route
    :param p_remove probability of removing random cities in an actual route
    :param rand_seeds: list of 3 random seeds to get always the same results
    :param use_replacement_set: if TRUE, when replacing an actual city, it chooses it from a smaller list
    of cities, called cities_for_replacement
    :param cities_for_replacement: (smaller) list of cities to be used to replace actual cities
    in order to enforce some repetition

    :return: a list of standard routes and a list of actual routes
    """

    random.seed(rand_seeds[0])  # to get always the same result

    standard_routes = []
    actual_routes = []

    # Define the standard routes (each route is a dictionary)
    for route_id in range(num_sroutes):
        sroute = {"id": f"s{route_id+1}", "route": []}

        # Define the cities to be visited for the current standard route
        ncities = random.randint(minncities, maxncities)
        cities_to_visit = random.sample(cities, ncities)

        # Create some modified lists of actual cities (store them in a list of lists)
        # replacing some cities in the current standard route. The number of lists in
        # the list actual_visited is how many actual routes we want to create for the
        # current standard route
        actual_visited = []

        # Number of actual routes for the current standard route
        nactual = round(random.normalvariate(average_num_actual, st_dev_actual))

        for _ in range(nactual):
            # Take the list of standard cities and modify just some
            actualcities = cities_to_visit.copy()
            # Here, we just replace some standard cities
            # The number of cities to modify is (p_cities_replace * ncities), rounded
            n_citiestomodify = math.floor(p_cities_replace * ncities)
            # n_citiestomodify = random.randint(0, math.floor(p_cities_replace * ncities))
            # Pick n_citiestomodify random positions inside the cities list and modify
            pos = random.sample(range(ncities), n_citiestomodify)
            for i in range(n_citiestomodify):
                # First we make sure we don't replace a city with another one that already appears
                # in the list of citites for the current actual route, unless there is no choice
                if use_replacement_set:
                    if cities_for_replacement is not None:
                        available_cities = [city for city in cities_for_replacement if city not in actualcities]
                        if not available_cities:
                            available_cities = cities_for_replacement
                        actualcities[pos[i]] = random.choice(available_cities)
                # Here we have tried to replace a city with another one in the cities_for_replacement
                # list, that is not already in the route. If there is no such available city, we
                # will allow for repetition
                else:
                    available_cities = [city for city in cities if city not in actualcities]
                    actualcities[pos[i]] = random.choice(available_cities)

            actual_visited.append(actualcities)

    # Create the json file for the standard routes

        num_trips = ncities - 1
        for i in range(num_trips):
            start_city = cities_to_visit[i]
            end_city = cities_to_visit[i+1]
            # Randomly select items from merchandise_types
            selected_items = random.sample(merchandise_types, random.randint(1, maxnumitems))
            # Create the merchandise dictionary with random quantities for selected items
            smerchandise = {item: random.randint(1, maxquantity) for item in selected_items}
            trip = {
                "from": start_city,
                "to": end_city,
                "merchandise": smerchandise
            }
            sroute["route"].append(trip)  # append the trip to the route of the current standard route

        standard_routes.append(sroute)  # append the current SR to the list of SRs

        # Define the json file for the nactual actual routes (here I am inside a standard route iteration)
        for aroute_id in range(nactual):
            aroute = {"id": f"a{route_id+1}_{aroute_id+1}",
                      "driver": random.choice(drivers),
                      "sroute": f"s{route_id+1}",
                      "route": []}

            # Define each actual route
            num_actrips = len(actual_visited[aroute_id]) - 1

            for i in range(num_actrips):
                start_city = actual_visited[aroute_id][i]
                end_city = actual_visited[aroute_id][i+1]
                amerchandise = standard_routes[route_id]["route"][i]["merchandise"].copy()

                # Modify merchandise in the actual route
                modified_merchandise = modify_merch(amerchandise, merchandise_types, maxquantity,
                                                    p_mod=p_mod, p_quant_change=p_quant_change)

                trip = {"from": start_city,
                        "to": end_city,
                        "merchandise": modified_merchandise}

                aroute["route"].append(trip)

            actual_routes.append(aroute)

    # Lastly, I can randomly add or remove cities from the actual routes
    random.seed(rand_seeds[1])  # so that I always remove and add the same cities

    # Randomly remove cities from the actual routes
    for r in range(len(actual_routes)):
        for t in range(len(actual_routes[r]["route"]) - 1, 0, -1):  # Iterate in reverse
            # This way, when I remove an item from the list, it doesn't affect
            # the indices of the items I haven't visited yet in the loop.
            if random.random() < p_remove:  # remove a city p_remove % of the times
                arrival_city = actual_routes[r]["route"][t]["to"]
                del actual_routes[r]["route"][t]
                actual_routes[r]["route"][t-1]["to"] = arrival_city

    # Add cities randomly from actual routes
    random.seed(rand_seeds[2])

    for r in range(len(actual_routes)):

        # Cities used in the current actual route
        used_cities = set(actual_routes[r]["route"][t]['from'] for t in range(len(actual_routes[r]['route'])))
        used_cities.update(set(actual_routes[r]["route"][t]['to'] for t in range(len(actual_routes[r]['route']))))

        t = 0
        while t < len(actual_routes[r]["route"]):
            if random.random() < p_add:  # add a city p_add % of the times
                if use_replacement_set:
                    available_cities = [city for city in cities_for_replacement if city not in used_cities]
                    if available_cities:
                        new_city = random.choice(available_cities)
                    else:
                        available_cities = [city for city in cities if city not in used_cities]
                        new_city = random.choice(available_cities)
                else:
                    available_cities = [city for city in cities if city not in used_cities]
                    new_city = random.choice(available_cities)

                # Update the "to" field of the original trip
                original_to_city = actual_routes[r]["route"][t]["to"]
                actual_routes[r]["route"][t]["to"] = new_city
                # Create a new trip with the "from" field set to the new city
                trip_to_add = {
                    "from": new_city,
                    "to": original_to_city,
                    "merchandise": modify_merch(actual_routes[r]["route"][t]["merchandise"],
                                                merchandise_types, maxquantity,
                                                p_mod=p_mod, p_quant_change=p_quant_change)
                }

                # Insert the new trip between the original trip and the next one
                actual_routes[r]["route"].insert(t + 1, trip_to_add)
                # Skip the next iteration since we have already processed the new trip
                t += 2
            else:
                t += 1

    return standard_routes, actual_routes
