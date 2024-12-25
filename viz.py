import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
data = pd.read_csv('result.csv')

# Extract density and pathfinding time columns
density = data.iloc[:, 0]  # Assuming density is the second column
pathfinding_time = data.iloc[:, -1]  # Assuming pathfinding time is the last column

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(density, pathfinding_time, marker='o', linestyle='-', color='b', label='Pathfinding Time')

# Adding labels and title
plt.xlabel('Density')
plt.ylabel('Pathfinding Time (s)')
plt.title('Pathfinding Time vs Density')
plt.grid(True)
plt.legend()

# Show the plot
plt.show()

count = data.iloc[:, -2]  # Assuming pathfinding time is the last column

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(density, count, marker='o', linestyle='-', color='b', label='Iter. count')

# Adding labels and title
plt.xlabel('Density')
plt.ylabel('Iter. count')
plt.title('Iter. count vs Density')
plt.grid(True)
plt.legend()

# Show the plot
plt.show()
