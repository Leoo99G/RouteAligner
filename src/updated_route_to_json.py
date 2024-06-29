import json

# In this file there are two functions that, given two lists of
# generated routes and merchandise, composes a json string with
# those routes and merchandise.

def generate_json(new_st_routes, upd_merch):
    """
    :param new_st_routes: list of updated standard routes (output of *generate_trip_sequence*)
    :param upd_merch: updated merchandise for the updated standard routes/trips
    :return: json string containing the updated standard routes
    """

    output_data = []

    for i, routes in enumerate(new_st_routes):
        st_route_id = f"s{i + 1}"
        route_data = {"id": st_route_id, "route": []}

        for j, route in enumerate(routes):
            from_city, to_city = route
            merchandise = upd_merch[i][j]

            route_info = {
                "from": from_city,
                "to": to_city,
                "merchandise": merchandise
            }

            route_data["route"].append(route_info)

        output_data.append(route_data)

    # Convert the data to a JSON string
    json_string = json.dumps(output_data, indent=2)

    return json_string


def generate_json_ideal_route_by_driver(new_routes, new_merch):
    """
    :param new_routes: list of ideal routes by driver (output of *generate_trip_sequence*)
    :param new_merch: ideal merchandise by driver
    :return: json string containing the updated standard routes
    """

    output_data = []

    for i, routes in enumerate(new_routes):
        driver = f"D{i + 1}"
        route_data = {"driver": driver, "route": []}

        for j, route in enumerate(routes):
            from_city, to_city = route
            merchandise = new_merch[i][j]

            route_info = {
                "from": from_city,
                "to": to_city,
                "merchandise": merchandise
            }

            route_data["route"].append(route_info)

        output_data.append(route_data)

    # Convert the data to a JSON string
    json_string = json.dumps(output_data, indent=2)

    return json_string
