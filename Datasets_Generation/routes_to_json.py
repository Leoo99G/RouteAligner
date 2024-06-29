import os
import json

def write_to_json(standard_file, actual_file, standard_name, actual_name, external_directory):

    # Get the absolute path to the script directory
    script_path = os.path.abspath(os.path.dirname(__file__))

    # Create the external directory if it doesn't exist
    external_path = os.path.join(script_path, '..', external_directory)
    os.makedirs(external_path, exist_ok=True)

    # Assuming 'standard_routes' has data
    if standard_file:
        # Save the JSON file in the external directory
        json_file_path = os.path.join(external_path, standard_name)
        try:
            with open(json_file_path, 'w') as json_file:
                json.dump(standard_file, json_file, indent=4)
            print(f"Standard routes file saved at: {os.path.abspath(json_file_path)}")
        except Exception as e:
            print(f"Error writing JSON file: {e}")
    else:
        print("No data to save.")


    # Assuming 'actual_routes' has data
    if actual_file:
        # Save the JSON file in the external directory
        json_file_path_actual = os.path.join(external_path, actual_name)
        try:
            with open(json_file_path_actual, 'w') as json_file_actual:
                json.dump(actual_file, json_file_actual, indent=4)
            print(f"Actual routes file saved at: {os.path.abspath(json_file_path_actual)}")
        except Exception as e:
            print(f"Error writing Actual JSON file: {e}")
    else:
        print("No data for actual_routes to save.")
