import pandas as pd


def dict_to_matrix(actual):
    # Step 1: Extract unique cities and merchandise items
    cities = set()
    merchandise_items = set()

    for route in actual:
        for trip in route["route"]:
            cities.add(trip["from"])
            cities.add(trip["to"])
            merchandise_items.update(trip["merchandise"].keys())

    # Step 2: Create a DataFrame with columns for each city and merchandise item
    columns = ['Set'] + list(cities) + list(merchandise_items)
    df = pd.DataFrame(columns=columns)

    # Step 3: Iterate through the routes and fill the DataFrame with 0s and 1s
    for route in actual:
        row = {col: 0 for col in columns}
        row['Set'] = route['id']

        for trip in route["route"]:
            # Mark cities as 1
            row[trip["from"]] = 1
            row[trip["to"]] = 1

            # Mark merchandise items as 1
            for item in trip["merchandise"]:
                row[item] = 1

        df = df.append(row, ignore_index=True)

        # Fill NaN values with 0, excluding the 'Set' column
        df.iloc[:, 1:] = df.iloc[:, 1:].fillna(0).astype(int)

    return df

def dict_to_set(route: dict) -> set:
    """
    Given a route, convert it to a set containing the cities
    visited and the merchandise items transported along the route.
    :param route: route (standard or actual): dictionary
    :return: set representation of that route
    """
    # Extract unique cities and merchandise items
    cities = set()
    merchandise_items = set()

    for trip in route['route']:
        cities.add(trip["from"])
        cities.add(trip["to"])
        merchandise_items.update(trip["merchandise"].keys())

    return cities.union(merchandise_items)



####### TESTING #########


actual_route = [
    {
        "id": "a1_1",
        "driver": "D23",
        "sroute": "s1",
        "route": [
            {"from": "Brindisi", "to": "Legnano", "merchandise": {"juice": 16}},
            {"from": "Legnano", "to": "Terni", "merchandise": {"avocado": 3, "toilet paper": 7, "mayonnaise": 22, "broccoli": 20}},
            {"from": "Terni", "to": "Monza", "merchandise": {"avocado": 3, "toilet paper": 7, "mayonnaise": 22, "broccoli": 20}}
        ]
    },
    {
        "id": "a1_2",
        "driver": "D45",
        "sroute": "s1",
        "route": [
            {"from": "Termoli", "to": "Milano", "merchandise": {"water": 14}},
            {"from": "Milano", "to": "Roma", "merchandise": {"chocolate": 3, "toilet paper": 7, "ketchup": 22, "broccoli": 20}},
            {"from": "Roma", "to": "Venezia", "merchandise": {"ice": 3, "ham": 7, "fish": 22, "honey": 20}}
        ]
    }
]

# mydf = dict_to_matrix(actual_route)
# print(mydf)
