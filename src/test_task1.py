# In this file we compare:
#  - the original standard routes and the actual routes
#  - the updated standard routes and the actual routes
# to see if there has been any improvement.

import json
from similarity import sr_similarities
import matplotlib.pyplot as plt

dataset_number = 3

# Original standard routes
or_st_routes = f'../data/standard{dataset_number}.json'
with open(or_st_routes, 'r') as file:
    original_standard_routes = json.load(file)

# Updated standard routes
up_st_routes = f'../results/recStandard{dataset_number}.json'
with open(up_st_routes, 'r') as file:
    updated_standard_routes = json.load(file)

# Actual routes
ac_routes = f'../data/actual{dataset_number}.json'
with open(ac_routes, 'r') as file:
    actual_routes = json.load(file)


sim1 = sr_similarities(original_standard_routes, actual_routes)
sim2 = sr_similarities(updated_standard_routes, actual_routes)

print(f'Average similarities of the SRs for dataset {dataset_number}:')
for i in range(len(sim1)):
    print(f's{i+1}: {sim1[i]} ', f'Rs{i+1}: {sim2[i]}')

avg_sim_orig = round(sum(sim1)/len(sim1), 4)
print('Average similarity with original standard routes: ', avg_sim_orig)
avg_sim_upd = round(sum(sim2)/len(sim2), 4)
print('Average similarity with recommended standard routes: ', avg_sim_upd)
avg_diff = round(sum(sim2)/len(sim2) - sum(sim1)/len(sim1), 3)
print(f'Average difference: {avg_diff}')

difference = [s2 - s1 > 0 for s2, s1 in zip(sim2, sim1)]
n_increase = sum(difference)
print(f'Number of standard routes for which we have increased the average similarity: '
      f'{n_increase}/{len(difference) if len(difference) > 0 else 0}')


difference = [s2 - s1 for s2, s1 in zip(sim2, sim1) if s2 > s1]
print(f'Average increase for the SRs we have improved: {round(sum(difference)/len(difference), 4) if len(difference) > 0 else 0}')


# Plotting the points and connecting them with lines
plt.plot(sim1, label='Original SRs similarities', linestyle='-')
plt.plot(sim2, label='Recommended SRs similarities', linestyle='-')


# Adding horizontal lines for the means
mean_sim1 = sum(sim1)/len(sim1)
mean_sim2 = sum(sim2)/len(sim2)
plt.axhline(mean_sim1, color='blue', linestyle='--')
plt.axhline(mean_sim2, color='orange', linestyle='--')

# Annotating the mean values
plt.text(len(sim1) - 0.5, mean_sim1, f'Mean: {mean_sim1:.2f}', color='blue', verticalalignment='center', backgroundcolor='white')
plt.text(len(sim2) - 0.5, mean_sim2, f'Mean: {mean_sim2:.2f}', color='orange', verticalalignment='center', backgroundcolor='white')


# Adding a box with annotations
# box_text = f'Avg. sim. for original SRs: {avg_sim_orig} \nAvg. sim. for recommended SRs: {avg_sim_upd}'
# plt.text(2, 0.38, box_text, bbox=dict(facecolor='white', alpha=0.5))

# # Plotting the points with lines connecting them
# for i in range(len(difference) - 1):
#     if difference[i] > 0:
#         plt.plot([i, i+1], [difference[i], difference[i+1]], marker='o', linestyle = '' , color='red')
#     else:
#         plt.plot([i, i+1], [difference[i], difference[i+1]], marker='o', linestyle = '', color='blue')


# Adding labels and title
plt.xlabel('Standard routes')
plt.ylabel('Average similarity with corresponding actual routes')
plt.title(f'SRs similarities for dataset {dataset_number}')

# Set y-axis limits
plt.ylim(0, 0.7)

# Adding a legend to identify the two lists
plt.legend()

# Save the plot as an image file (e.g., PNG)
plt.savefig(f'../Plots/avg_sims_{dataset_number}.jpg')

# Display the plot
# plt.show()
