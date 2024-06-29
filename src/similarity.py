
# This file contains various functions that are used to compute similarities among routes


def jaccard_sim_dict(dict1: dict, dict2: dict) -> float:
    """
    This function computes the Jaccard similarity between two
    Python dictionaries (or multisets) of merchandise items.
    :param dict1: dictionary of (item, quantity) pairs
    :param dict2: dictionary of (item, quantity) pairs
    :return: Jaccard similarity of the two dictionaries
    """
    num = sum(min(dict1.get(item, 0), dict2.get(item, 0)) for item in set(dict1) & set(dict2))
    den = sum(max(dict1.get(item, 0), dict2.get(item, 0)) for item in set(dict1) | set(dict2))
    return num / den if den != 0 else 0


def similarity_sr_ar(sroute: dict, aroute: dict, w1: float = 0.5) -> float:
    """
    This function computes the similarity between a standard route and an actual route.
    :param sroute: standard route given as a Python dictionary (we assume
    each city is visited just once)
    :param aroute: actual route given as a Python dictionary (cities can be
    visited multiple times)
    :param w1: weight for the 1st similarity (Jaccard similarity for the visited cities)
               (1-w1) is the weight for the 2nd similarity (J_merch)
    :return: similarity value (float) between 0 and 1
    """

    # Compute J_cities

    standard_visited_cities = set(trip['from'] for trip in sroute['route'])
    standard_visited_cities.update(trip['to'] for trip in sroute['route'])

    actual_visited_cities = set(trip['from'] for trip in aroute['route'])
    actual_visited_cities.update(trip['to'] for trip in aroute['route'])

    intersection = len(standard_visited_cities.intersection(actual_visited_cities))
    union = len(standard_visited_cities.union(actual_visited_cities))

    j_cities = intersection / union if union else 0

    # Compute J_merch

    sim_scores_merch = []
    ac_dest_cities = [trip['to'] for trip in aroute['route']]

    for st_trip in sroute['route']:
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


def sr_similarities(standard: list, actual: list, w1: float = 0.5) -> list:
    """
    This function takes a list of SRs and a list of ARs and computes,
    for every SR, the average similarities with the ARs that implement
    that SR.
    :param standard: list of SRs
    :param actual: list of ARs
    :param w1: weight for the weighted average for the similarity measure
    :return: list (the length of the list is the number of standard routes in "standard")
    """
    similarities = []
    for sroute in standard:
        current_sroute_sim = []
        for aroute in actual:
            if aroute['sroute'] == sroute['id']:
                current_sroute_sim.append(similarity_sr_ar(sroute, aroute, w1))
        mean = sum(current_sroute_sim) / len(current_sroute_sim)
        similarities.append(round(mean, 4))
    return similarities
