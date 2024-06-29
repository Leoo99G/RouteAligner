import pandas as pd
from mlxtend.frequent_patterns import apriori


# Here there are some functions that collectively take the set of actual
# routes and create a modified/updated version of the standard routes.


# The function *recommend_routes*:
# - takes a Pandas dataframe of actual routes,
# - splits them based on their standard route id
# - passes each batch of actual routes to the function *frequent*,
#   that creates a frequency dictionary of trips;
# - the freq. dictionary is passed to the function *build_new_route*,
#   that builds an updated version of the current standard route.
# - The function *update_merchandise* computes the merchandise for
#   the updated standard routes by averaging on the frequent items of
#   the actual trips


def frequent(df: pd.DataFrame, freq: float) -> dict:
    """
    :param df: dataframe of "from" and "to" trips (includes also the route_id)
    :param freq: percentage above which a trip is considered frequent (just the
    trips that are frequent are kept in the output dictionary)
    :return: sorted frequency dictionary of the form {("from city", "to city"): n}
    where n is the number of times that trip appears in the actual routes related
    to the current standard route
    """
    frequency_dict = {}

    n = len(df['route_id'].unique())  # Number of actual routes

    for index, row in df.iterrows():
        from_location = row['from'].strip()
        to_location = row['to'].strip()
        route_pair = (from_location, to_location)

        frequency_dict[route_pair] = frequency_dict.get(route_pair, 0) + 1

    # Filter the dictionary based on the frequency threshold
    filtered_frequency_dict = {k: v for k, v in frequency_dict.items() if v / n >= freq}

    # Keep just the items whose key contains two different cities
    filtered_frequency_dict = {key: value for key, value in filtered_frequency_dict.items() if key[0] != key[1]}

    # Sort the filtered dictionary by values in descending order
    sorted_frequency_dict = dict(sorted(filtered_frequency_dict.items(), key=lambda item: item[1], reverse=True))
    return sorted_frequency_dict


def generate_trip_sequence(freqdic, max_length: int = None) -> list:
    """
    :param freqdic: dictionary of frequent trips among the actual routes (output of *frequent* function)
    :param max_length: "maximum" length of an updated standard route
    :return: updated standard route (list) based on the frequency dictionary given as input
    """
    new_route = []
    first_key = list(freqdic.keys())[0]
    new_route.append(first_key)
    last_city = first_key[1]  # Last visited city (starting city of next trip)
    start_city = first_key[0]  # City already visited

    # Delete all the trips that contain the already visited cities
    for key in list(freqdic.keys()):
        if start_city in key:
            del freqdic[key]

    while freqdic and (max_length is None or len(new_route) < max_length):

        selected_trip = None
        # Check if the first trip starts with the last visited city (if there is one)
        first_key = list(freqdic.keys())[0]
        if first_key[0] == last_city:
            selected_trip = first_key

        # If there is such trip, add it to the new_route list
        if selected_trip:
            new_route.append(selected_trip)
            start_city = selected_trip[0]
            last_city = selected_trip[1]
            for key in list(freqdic.keys()):
                if start_city in key:
                    del freqdic[key]
        else:
            for key in list(freqdic.keys()):
                if last_city == key[1]:
                    del freqdic[key]
            if freqdic:
                dummy_start = last_city
                dummy_end = str(list(freqdic.keys())[0][0])
                dummy_trip = (dummy_start, dummy_end)
                new_route.append(dummy_trip)
                new_route.append(list(freqdic.keys())[0])

                start_city = dummy_end
                last_city = list(freqdic.keys())[0][1]

                for key in list(freqdic.keys()):
                    if start_city in key:
                        del freqdic[key]
            else:
                return new_route

    return new_route


def update_merchandise(updated_route: list, df: pd.DataFrame, min_support=0.4) -> list:
    """
    :param updated_route: list of updated routes (output of *generate_trip_sequence*)
    :param df: portion of actual routes dataframe used to compute the updated merchandise
    :param min_support: support above which an item of merchandise is considered frequent
    :return: list containing a dictionary of merchandise for every trip in the updated standard route
    """
    updated_merch = []

    # Iterate over the updated standard trips
    for st_trip in updated_route:
        start_city = st_trip[0]
        end_city = st_trip[1]
        # Extract the portion of dataframe with these 'from' and 'to' cities
        # merch_df = df[(df['from'] == start_city) & (df['to'] == end_city)]
        merch_df = df[(df['from'] == start_city) & (df['to'] == end_city)]
        merch_df = merch_df.drop(['from', 'to'], axis=1)
        boolean_merch = merch_df.astype(bool)
        frequent_items = apriori(boolean_merch, min_support=min_support, use_colnames=True, max_len=1)
        # current_updated_merch = {str(value): merch_df[value].mean() for value in frequent_items['itemsets']}
        current_updated_merch = {str(list(value)[0]): round(merch_df[value].mean().values[0])
                                 for value in frequent_items['itemsets']}

        updated_merch.append(current_updated_merch)

    return updated_merch


def recommend_routes(actualdf: pd.DataFrame, standard_df: pd.DataFrame, freq: float):
    """
    :param actualdf: Pandas dataframe of actual routes
    :param standard_df: Pandas dataframe of standard routes
    :param freq: percentage above which to keep in the frequency dictionary
    a trip that appears in the actual routes
    :return: list of updated standard routes and updated merchandise
    """
    new_st_routes = []
    updated_merchandise = []

    n_st_routes = len(actualdf['sroute'].unique())  # Number of standard routes

    for sroute_id in range(1, n_st_routes + 1):

        # Max length of each updated standard route is the length of the
        # corresponding original standard route (+1 in some cases, when a dummy trip is inserted)
        max_length = standard_df[standard_df['route_id'] == ('s' + str(sroute_id))].shape[0] + 2

        # Extract the actual routes with current standard route id
        # and keep just the columns 'route_id', 'from', 'to'.
        filtered_df = actualdf[actualdf['sroute'] == 's' + str(sroute_id)][['route_id', 'from', 'to']]

        # Create the frequency dictionary
        frequency_dictionary = frequent(filtered_df, freq)

        # Create the new sequence of trips
        new_route = generate_trip_sequence(frequency_dictionary, max_length=max_length)

        # Add it to the new version of standard routes
        new_st_routes.append(new_route)

        # Define the merchandise for the current updated standard route

        # Extract just the actual trips for the current standard route
        merchandise_df = actualdf[actualdf['sroute'] == 's' + str(sroute_id)]

        # Remove columns not needed before passing the dataframe to *update_merchandise*
        columns_not_needed = ['route_id', 'sroute', 'driver']
        merchandise_df = merchandise_df.drop(columns=columns_not_needed)

        updated_current_merchandise = update_merchandise(new_route, merchandise_df)
        updated_merchandise.append(updated_current_merchandise)

    return new_st_routes, updated_merchandise
