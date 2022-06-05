# Import Packages
import os, sys
from pathlib import Path
from collections import defaultdict, deque
import math

# ----------------------------------------------------------------
# Read in command line arguments
# ----------------------------------------------------------------

filenumber = int(sys.argv[1])
inputfolder = Path(sys.argv[2])
outputfolder = Path(sys.argv[3])

print("Command line arguments:")
print("File number (range: [0, 359]):", filenumber)
print("Input folder:", inputfolder)
print("Output folder:", outputfolder)

# Define list of solved inputs
list_solved_inputs = [157, 216, 1, 309, 300, 123, 103, 229, 230, 349, 283, 38, 221, 261, 263, 297, 164, 74, 341, 233, 109, 271, 265, 214, 56, 155, 11, 106, 86, 137, 91, 332, 191, 241, 6, 272, 307, 228, 132, 167, 258, 231, 65, 213, 277, 180, 292, 104, 147, 195, 188, 223, 17, 122, 142, 63, 268, 287, 359, 353, 27, 20, 334, 289, 165, 227, 151, 196, 14, 174, 351, 269, 84, 290, 327, 199, 41, 28, 108, 219, 318, 322, 358, 189, 163, 222, 12, 94, 59, 62, 110, 124, 57, 133, 314, 47, 77, 69, 282, 36, 168, 224, 324, 336, 306, 131, 144, 53, 60, 348, 212, 177, 37, 33, 242, 311, 8, 243, 31, 237, 42, 126, 34, 127, 238, 152, 130, 331, 225, 254, 85, 46, 226, 140, 138, 161, 111, 338, 236, 54, 317, 284, 119, 96, 9, 355, 18, 120, 128, 206, 266, 185, 298, 50, 21, 160, 357, 232, 239, 256, 176, 194, 121, 182, 90, 114, 88, 270, 255, 202, 70, 98, 250, 173, 87, 186, 141, 35, 352, 2, 112, 329, 335, 245, 55, 64, 356, 235, 193, 259, 26, 81, 267, 240, 319, 323, 249, 264, 285, 295, 80, 192, 291, 273, 66, 58, 350, 44, 10, 150, 253, 75, 337, 92, 181, 198, 316, 217, 197, 30, 343, 299, 23, 73, 288, 347, 19, 301, 205, 325, 204, 158, 179, 247, 172, 178, 83, 220, 25, 39, 183, 125, 339, 99, 210, 5, 209, 49, 303, 95, 342, 148, 101, 333, 171, 208, 184, 135, 302, 115, 129, 340, 315, 345, 321, 16, 139, 234, 153, 320, 82, 154, 286, 280, 207, 76, 134, 52, 113, 293, 97, 48, 102, 200, 257, 68, 170, 166, 107, 100, 67, 89, 326, 156, 344, 7, 294, 15, 203, 175, 260, 276, 305, 304, 275, 79, 262, 29, 71, 72, 187, 251, 149, 244, 279, 40, 118, 136, 313]

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
        return -1
    new_current_time = start_time_at_next_node + ride_durations[next_node]
    # print("next_node:", next_node)
    # print("ride_durations[next_node]:", ride_durations[next_node])
    travel_time_to_origin = edges[(next_node, 0)]
    earliest_new_finish_time = new_current_time + travel_time_to_origin

    if earliest_new_finish_time <= 1440:
        return new_current_time
    else:
        return -1

# ----------------------------------------------------------------
# Pre-process input to get graph, edges and important information
# ----------------------------------------------------------------

# Import input only if it has not been already solved
if filenumber in list_solved_inputs:
    print("file number is in list of solved inputs. Skipping file, best solution has already been found!")
    print("---")
    sys.exit()
    
# Import input only if index = specified file number
for index, item in enumerate(inputfolder.iterdir()):
    # print("Index:", index)
    # print("Input File Processed:", item)
    if index == filenumber:
        item_filenumber = item
        print("Input file:", item_filenumber)

        # Get the output file path
        stem_filenumber = item.stem
        outputfilename = stem_filenumber + ".out"
        outputfilepath = Path(outputfolder / outputfilename)

        # Skip file if output already exists, since brute force finds the best solution
        if os.path.exists(outputfilepath):
            print("Output already exists, skipping file")
            print("-------")
            sys.exit()
        else:
            print("Output does not currently exist, processing file")
            print("-------")

        # Read the input file
        with open(item) as f:
            N = int(f.readline())
            # Append the origin to the rides
            rides = [[200, 200, 0, 0, 0, 0]] + [[int(i) for i in line.split()] for line in f]
            # print("Number of rides:", N)
            # print("Rides:\n", rides)

# Create list of nodes, with node 0 being the origin (200, 200)
# This implies that index of node = actual node number
list_nodes = [i for i in range(N+1)]

# Initialize list of feasible nodes
feasible_nodes = [i for i in range(1, N+1)]
# print(feasible_nodes)

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
# Initialize loop
# ----------------------------------------------------------------

# Initialize queue
queue = deque()

# Initialize remaining feasible nodes 
remaining_feasible_nodes = []

# Initialize sequence of nodes visited
nodes_visited = []

# Initialize score
score = 0

# Find all feasible next nodes
for i in feasible_nodes.copy():
    # print(i)
    # Remove all nodes with 0 utility
    if utilities[i] == 0:
        feasible_nodes.remove(i)
    else:
        # Check if nodes are feasible
        new_current_time = check_feasible(0, 0, i, edges, start_times, end_times, ride_durations)
        
        # Remove all infeasible nodes
        if new_current_time == -1:
            # print("Infeasible:", nodes_visited + [i])
            feasible_nodes.remove(i)
        # Keep track of all remaining feasible nodes 
        else:
            # print("Feasible:", nodes_visited + [i])
            new_score = score + utilities[i]
            remaining_feasible_nodes.append((i, new_current_time, new_score))

# For each remaining feasible node, add the node to the list of nodes visited, 
# and add it to the queue with the updated list of remaining feasible nodes, and the new current time
for i, new_current_time, new_score in remaining_feasible_nodes:
    new_nodes_visited = nodes_visited.copy()
    new_nodes_visited.append(i)
    new_feasible_nodes = feasible_nodes.copy()
    new_feasible_nodes.remove(i)
    queue.append((new_nodes_visited, new_feasible_nodes, new_current_time, new_score))

# print("Queue:", queue)

# ----------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------

best_score = 0
best_sequence = []
print("Initial best score:", score)
print("Initial best sequence:", best_sequence)
print("---")

while len(queue) > 0:
    nodes_visited, feasible_nodes, current_time, score = queue.pop()
    # print(nodes_visited)
    current_node = nodes_visited[-1]

    # Initialize remaining feasible nodes 
    remaining_feasible_nodes = []

    # Find all feasible next nodes
    for i in feasible_nodes.copy():
        
        # Check if nodes are feasible
        new_current_time = check_feasible(current_time, current_node, i, edges, start_times, end_times, ride_durations)

        # Remove all infeasible nodes
        if new_current_time == -1:
            # print("Infeasible:", nodes_visited + [i])
            # print("Score of infeasible sequence:", score + utilities[i])
            feasible_nodes.remove(i)
        
        # Keep track of all remaining feasible nodes 
        else:
            new_score = score + utilities[i]
            remaining_feasible_nodes.append((i, new_current_time, new_score))
            # print("Feasible:", nodes_visited + [i])
            # print("remaining_feasible_nodes:", remaining_feasible_nodes)

    # If there are at least 2 remaining feasible nodes (and hence more points to be earned in the next round), add to the queue
    if len(remaining_feasible_nodes) > 1:
        # For each remaining feasible node, add the node to the list of nodes visited, 
        # and add it to the queue with the updated list of remaining feasible nodes, and the new current time
        for i, new_current_time, new_score in remaining_feasible_nodes:
            new_nodes_visited = nodes_visited.copy()
            new_nodes_visited.append(i)
            new_feasible_nodes = feasible_nodes.copy()
            new_feasible_nodes.remove(i)
            queue.append((new_nodes_visited, new_feasible_nodes, new_current_time, new_score))
            if new_score > best_score:
                best_score = new_score
                best_sequence = new_nodes_visited.copy()
                print("New best score:", best_score)
                print("New best sequence (ongoing):", best_sequence)
                print("Time taken:", new_current_time + edges[(i,0)])
                print("---")

    # Else if there is only 1 remaining feasible node, add the score from this node, and end the sequence. Update the score if it is higher than the current max.
    elif len(remaining_feasible_nodes) == 1:
        i, new_current_time, new_score = remaining_feasible_nodes[0]
        new_nodes_visited = nodes_visited.copy()
        new_nodes_visited.append(i)
        if new_score > best_score:
            best_score = new_score
            best_sequence = new_nodes_visited.copy()
            print("New best score:", best_score)
            print("New best sequence (ended):", best_sequence)
            print("Time taken:", new_current_time + edges[(i,0)])
            print("---")

    # Else the sequence cannot proceed further, and the score cannot be further increased. Update the score if it is higher than the current max.
    else:
        if score > best_score:
            best_score = score
            best_sequence = nodes_visited.copy()
            print("New best score:", best_score)
            print("New best sequence (ended):", best_sequence)
            print("Time taken:", current_time + edges[(current_node,0)])
            print("---")

# ----------------------------------------------------------------
# Summary
# ----------------------------------------------------------------

print("Main loop completed!")

# Print Summary
print("")
print("--------------")
print("Summary:")
print("file number:", filenumber)
print("Input file:", item_filenumber)
print("Final best score:", best_score)
print("Final best sequence:", best_sequence)
print("---")
print("Output to copy:")
print(len(best_sequence))
print(*best_sequence)

# ----------------------------------------------------------------
# Save best sequence into an .out file
# ----------------------------------------------------------------

print("--------------")
best_sequence = [str(node) for node in best_sequence]
with open(outputfilepath, "w") as f1:
    # Writing data to a file
    f1.write(str(len(best_sequence)) + "\n")
    f1.write(' '.join(best_sequence))
print("Saved best sequence to:", outputfilepath)
print("--------------")
