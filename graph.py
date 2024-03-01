import matplotlib.pyplot as plt
import json

# Load data from a file
file_path = 'graph.json' 
with open(file_path, 'r') as file:
    loaded_data = json.load(file)

# Extract relevant information
incorrect_data = [entry["incorrect"] for entry in loaded_data]
elapsed_time_data = [entry["elapsed_time"] for entry in loaded_data]

# Plot the data
plt.scatter(incorrect_data, elapsed_time_data, marker='o', color='blue')
plt.xlabel('Number of Incorrect')
plt.ylabel('Elapsed Time (seconds)')
plt.title('Number of Incorrect vs Elapsed Time')
plt.grid(True)
plt.show()
