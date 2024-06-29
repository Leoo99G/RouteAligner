import pandas as pd
from update_routes import frequent, generate_trip_sequence, update_merchandise


def ideal_routes_by_driver(actualdf: pd.DataFrame, freq: float = 0):
    """
    :param actualdf: Pandas dataframe of actual routes
    :param freq: percentage above which to keep trips that appears in the actual
    routes in the frequency dictionary
    :return: list of new standard routes and merchandise
    """
    new_routes = []
    new_merchandise = []

    n_drivers = len(actualdf['driver'].unique())  # Number of drivers

    for driver in range(1, n_drivers + 1):

        # Extract the actual routes with current driver
        # and keep just the columns 'route_id', 'from', 'to'.
        filtered_df = actualdf[actualdf['driver'] == f'D{driver}'][['route_id', 'from', 'to']]
        # print(filtered_df)

        # Max length of each ideal route for the current driver is the average length
        # of the actual routes implemented by that driver (+1 in some cases, when a dummy trip
        # is inserted)
        # Group by 'id' and calculate the size (number of rows) for each group
        max_length = round(filtered_df.groupby('route_id').size().mean())
        # print('Max length: ', max_length)

        # Create the frequency dictionary from the trips of the current driver
        frequency_dictionary = frequent(filtered_df, freq)
        # print(frequency_dictionary)

        # Create the new sequence of trips
        new_route = generate_trip_sequence(frequency_dictionary, max_length=max_length)
        # print(new_route)

        # Add it to the new version of standard routes
        new_routes.append(new_route)

        # Define the merchandise for the current updated standard route

        # Extract just the actual trips for the current standard route
        merchandise_df = actualdf[actualdf['driver'] == f'D{driver}']

        # Remove columns not needed before passing the dataframe to *update_merchandise*
        columns_not_needed = ['route_id', 'sroute', 'driver']
        merchandise_df = merchandise_df.drop(columns=columns_not_needed)

        updated_current_merchandise = update_merchandise(new_route, merchandise_df, min_support=0.2)
        new_merchandise.append(updated_current_merchandise)

    return new_routes, new_merchandise


# # Load the input file actual.json
# actual_routes_df = pd.read_csv('../Routes_tables/actual_routes_table_8.csv')
#
#
# ideal_routes, ideal_merchandise = ideal_routes_by_driver(actual_routes_df)
#
# print(f'Ideal routes by driver ({len(ideal_routes)}):')
# print(ideal_routes)
#
# print(f'Ideal merchandise by driver ({len(ideal_merchandise)}):')
# print(ideal_merchandise)
