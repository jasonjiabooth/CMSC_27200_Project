# Import Packages
import pandas as pd, numpy as np
import os, sys
from pathlib import Path
from collections import defaultdict
import math

inputfilepath = Path(sys.argv[1])
outfilepath = Path(sys.argv[2])

print("Input File Processed:", inputfilepath)
print("Output File Processed:", outfilepath)

# Example:
# python C:\Users\jasonjia\Dropbox\02_jason_personal\cmsc_courses\cmsc_27200\project\03_find_solutions\code\compute_time_and_score.py C:\Users\jasonjia\Dropbox\02_jason_personal\cmsc_courses\cmsc_27200\project\03_find_solutions\all_inputs\RubberDucks_small1.in C:\Users\jasonjia\Dropbox\02_jason_personal\cmsc_courses\cmsc_27200\project\03_find_solutions\all_outputs\all_outputs_manual\RubberDucks_small1.out

# ----------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------

# Function to calculate travel time = distance (rounded up to the nearest int)
def travel_time(x_1, y_1, x_2, y_2):
    travel_time = math.ceil(((x_2 - x_1)**2 + (y_2 - y_1)**2)**0.5)
    return travel_time

# Check if going to the next node is feasible
# Feasible if current time + travel time (to next node) + waiting time + ride duration + travel time (back to origin) <= 1440
# If feasible, return new current time = current time + travel time + waiting time + ride duration
# Else, return -1
def check_feasible(current_time, current_node, next_node, edges, start_times, end_times, ride_durations):
    travel_time_to_next_node = edges[(current_node, next_node)]
    start_time_at_next_node = max(current_time+travel_time_to_next_node, start_times[next_node])
    if start_time_at_next_node > end_times[next_node]:
        print("start_time_at_next_node:", start_time_at_next_node, "exceeded end_times[next_node]:", end_times[next_node])
        return -1
    new_current_time = start_time_at_next_node + ride_durations[next_node]
    # print("next_node:", next_node)
    # print("ride_durations[next_node]:", ride_durations[next_node])
    travel_time_to_origin = edges[(next_node, 0)]
    earliest_new_finish_time = new_current_time + travel_time_to_origin

    if earliest_new_finish_time <= 1440:
        return new_current_time
    else:
        print("earliest_new_finish_time:", earliest_new_finish_time)
        return -1

# Read input file
with open(inputfilepath) as f:
    N = int(f.readline())
    # Append the origin to the rides
    rides = [[200, 200, 0, 0, 0, 0]] + [[int(i) for i in line.split()] for line in f]
    # print("Number of rides:", N)
    # print("Rides:\n", rides)

# Import out file
with open(outfilepath) as f:
        N_out = int(f.readline())
        # Append the origin to the rides
        rides_out = [int(i) for i in f.readline().split()]
        print("Number of rides:", N_out)
        print("Rides:\n", rides_out)

print("-------")

# ----------------------------------------------------------------
# Pre-process input to get graph, edges and important information
# ----------------------------------------------------------------

# Create list of nodes, with node 0 being the origin (200, 200)
# This implies that index of node = actual node number
list_nodes = [i for i in range(N+1)]

# Initialize list of feasible nodes
feasible_nodes = [i for i in range(1, N+1)]

# Create list of edges
edges = defaultdict(list)
for i in range(N+1):
    for j in range(N+1):
        edges[(i,j)] = travel_time(rides[i][0], rides[i][1], rides[j][0], rides[j][1])

# print(edges)

# Create list of start times, end times, utilities, and ride durations
start_times = defaultdict(list)
end_times = defaultdict(list)
utilities = defaultdict(list)
ride_durations = defaultdict(list)

for i in range(1, N+1):
    start_times[i] = rides[i][2]
    end_times[i] = rides[i][3]
    utilities[i] = rides[i][4]
    ride_durations[i] = rides[i][5]

# ----------------------------------------------------------------
# Check output
# ----------------------------------------------------------------

# Get score
score = 0

# Get total time taken
current_time = 0
start_node = 0
feasible = 1
for i in rides_out:
    print("---")
    print("Now travelling to node", i)
    print("Coordinates: (", rides[i][0], ",", rides[i][1], ")")
    print("Start, End times: (", start_times[i], ",", end_times[i], ")")
    travel_time = edges[(start_node, i)]
    ride_duration = ride_durations[i]
    new_current_time = check_feasible(current_time, start_node, i, edges, start_times, end_times, ride_durations)
    score = score + utilities[i]

    if new_current_time == -1:
        feasible = 0
        print("Not feasible")
        print("travel time:", travel_time)
        print("ride duration:", ride_duration)
        break
    else:
        print("Feasible")
        print("travel time:", travel_time)
        print("new current time:", new_current_time)
        print("ride duration:", ride_duration)
        print("waiting time:", new_current_time - current_time - travel_time - ride_duration)
        print("score:", score)

    start_node = i
    current_time = new_current_time

print("-------")
print("Summary:")
if feasible == 1:
    print("Sequence is feasible")
    print("Score:", score)
    print("Total time taken:", new_current_time + edges[(rides_out[-1], 0)])
else:
    print("Sequence is not feasible")
    print("Score (if feasible):", score)