import pandas as pd
import matplotlib.pyplot as plt

# Sample data in a DataFrame
data = pd.DataFrame({
    'Task': ['Task 1', 'Task 2', 'Task 3', 'Task 4'],
    'Start': [10, 20, 30, 40],
    'End': [15, 25, 35, 50]
})

# Create a figure and axis
fig, ax = plt.subplots(figsize=(6, 10))

# Set the color for the bars
bar_color = (0, 0.447, 0.741)

# Plot the bars with rounded edges
for i, row in data.iterrows():
    task, start, end = row['Task'], row['Start'], row['End']
    bar = ax.barh(i, end - start, left=start, color=bar_color, height=0.2, capstyle='round', joinstyle='round')

# Set the y-axis limits
ax.set_ylim(-1, len(data))

# Add labels and title
ax.set_xlabel("Time")
ax.set_yticks(range(len(data)))
ax.set_yticklabels(data['Task'])
ax.set_title("Gantt Chart", rotation=90)

# Add grid lines
ax.grid(axis='x', linestyle='--')

# Adjust the spacing between subplots
plt.subplots_adjust(left=0.2, bottom=0.1)

# Rotate the x-axis labels
plt.xticks(rotation=90)

# Display the chart
plt.show()