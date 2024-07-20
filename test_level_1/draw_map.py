import matplotlib.pyplot as plt
import numpy as np

def read_map_from_file(file_path):
    with open(file_path, 'r') as file:
        # Read the first line for n and m
        first_line = file.readline().strip()
        n, m = map(int, first_line.split())
        
        map_2d = []
        for line in file:
            row = line.strip().split()
            # Convert numeric strings to integers
            row = [int(cell) if cell.isdigit() or cell == '-1' else cell for cell in row]
            map_2d.append(row)
    
    return n, m, map_2d

def plot_map(map_2d, file_name='map.png'):
    # Create a color map: white for 0, blue for -1, green for S, red for G
    color_map = {
        0: (1, 1, 1),  # white
        -1: (0, 0, 1), # blue
        'S': (0, 1, 0), # green
        'G': (1, 0, 0)  # red
    }

    # Convert the map to an array of RGB values
    rgb_map = np.zeros((len(map_2d), len(map_2d[0]), 3))
    for i, row in enumerate(map_2d):
        for j, cell in enumerate(row):
            rgb_map[i, j] = color_map[cell]

    # Plot the map
    plt.imshow(rgb_map, aspect='equal')
    plt.axis('off')  # Turn off the axis
    plt.savefig(file_name, bbox_inches='tight', pad_inches=0)
    plt.show()

# Read the map from input.txt
file_path = "test_level_1\input5_level1.txt"
n, m, map_2d = read_map_from_file(file_path)

print(f"Dimensions read from file: n={n}, m={m}")
print(f"Dimensions of map_2d: {len(map_2d)} rows, {len(map_2d[0])} columns")

# Plot the map and save it as an image
plot_map(map_2d)
