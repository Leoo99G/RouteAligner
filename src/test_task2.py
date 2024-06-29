import json
from collections import Counter
import editdistance
import matplotlib.pyplot as plt
from basictop5routes import basic_five_best_routes


dataset_number = 4
# Load the recStandard.json file just created
with open(f'../data/standard{dataset_number}.json', 'r') as file:
    st_routes = json.load(file)
# Load the recStandard.json file just created
with open(f'../data/actual{dataset_number}.json', 'r') as file:
    ac_routes = json.load(file)
# Load the recStandard.json file just created
with open(f'../results/recStandard{dataset_number}.json', 'r') as file:
    upd_st_routes = json.load(file)

# my top5
with open(f'../results/driver{dataset_number}.json', 'r') as file:
    mytop5 = json.load(file)


# Optimal top 5
basictop5list = basic_five_best_routes(actual_routes=ac_routes,
                                       standard_routes=st_routes,
                                       updated_standard_routes=upd_st_routes)


# Count how many SRs from the original and updated versions of the SRs are included
num_s = 0
num_Rs = 0
for d in mytop5:
    for r in d['routes']:
        if r[0] == 's':
            num_s += 1
        else:
            num_Rs += 1

print(f'Number of SRs suggested from the original SRs: {num_s}')
print(f'Number of SRs suggested from the updated SRs: {num_Rs}')


# Count for how many drivers SR number 1 in the optimal list has been guessed in my top 5 list
guessed_first = 0
for d1 in mytop5:
    for d2 in basictop5list:
        if d1['driver'] == d2['driver'] and d1['routes'][0] == d2['routes'][0]:
            guessed_first += 1
print(f'First route guessed for {guessed_first}/{len(mytop5)} drivers.')


# Count of shared items
shared_items_counts = []
for driver_list in mytop5:
    for basic_driver_list in basictop5list:
        if driver_list['driver'] == basic_driver_list['driver']:
            # Count how many of the optimal SR are in the suggested top 5
            set_mytop5 = set(driver_list['routes'])
            set_optimaltop5 = set(basic_driver_list['routes'])
            n_included = 0
            for sr in set_optimaltop5:
                if sr in set_mytop5:
                    n_included += 1

            shared_items_counts.append(round(n_included/5, 2))


print('Number of SRs in the optimal top 5 list that are also in the suggested top 5 list:')
print(shared_items_counts)
avg_count = round(sum(shared_items_counts)/len(shared_items_counts), 2)
print('Average count: ', avg_count)


# Plotting Jaccard similarities

# Counting the frequency of each value
counter = Counter(shared_items_counts)
# Extracting unique values and their frequencies
values, frequencies = zip(*counter.items())
# Calculating relative frequencies
total_points = len(shared_items_counts)
relative_frequencies = [freq / total_points for freq in frequencies]

plt.figure(figsize=(4.1, 4))
plt.bar(values, relative_frequencies, color='lightblue', width=0.1)
plt.xlabel('Shared items count')
plt.ylabel('Relative frequency')
# Set tick positions and labels
values = list(values)
values.insert(0, 0)
values.append(1)
plt.xticks([val for val in values], [f'{val:.2f}' for val in values])
plt.tight_layout()
# Save the plot
plt.savefig(f'../Plots/barplotshared_{dataset_number}')


# Edit distance method


def map_lists_to_strings(list1, list2):
    """
    This function takes two lists of strings and maps each string to a character.
    This is needed to compute the edit distance among the resulting 5-character strings.
    :param list1: list of strings
    :param list2: list of strings
    :return: two 5-character strings
    """
    # Concatenate the lists before enumerating
    combined_list = list1 + list2

    # Create a mapping of strings to characters
    string_to_char_mapping = {string: chr(ord('a') + idx) for idx, string in enumerate(combined_list)}

    # Map strings to characters
    mapped_list1 = ''.join(string_to_char_mapping[string] for string in list1)
    mapped_list2 = ''.join(string_to_char_mapping[string] for string in list2)

    return mapped_list1, mapped_list2


edit_dist = []
for driver_list in mytop5:
    for basic_driver_list in basictop5list:
        if driver_list['driver'] == basic_driver_list['driver']:
            # Compare the two top5 lists using edit distance
            list1 = driver_list['routes']
            list2 = basic_driver_list['routes']
            string1, string2 = map_lists_to_strings(list1, list2)
            edit_dist.append(editdistance.eval(string1, string2))

print('Edit distance between the two top 5 lists for each driver:')
print(edit_dist)
avg_edit = round(sum(edit_dist)/len(edit_dist), 2)
print('Average edit dist: ', avg_edit)


# Plotting edit distance

# Counting the frequency of each value
counter = Counter(edit_dist)
# Extracting unique values and their frequencies
values, frequencies = zip(*counter.items())
# Calculating relative frequencies
total_points = len(edit_dist)
relative_frequencies = [freq / total_points for freq in frequencies]

# Creating a bar plot
plt.figure(figsize=(4, 4))
plt.bar(values, relative_frequencies, color='lightblue', width=0.4)
values = list(values)
values = (0,1,2,3,4,5)
plt.xlabel('Edit distance')
plt.ylabel('Relative frequency')
# Set tick positions and labels
plt.xticks([val for val in values], [f'{val:.2f}' for val in values])
plt.tight_layout()
plt.savefig(f'../Plots/barplotedit_{dataset_number}')
