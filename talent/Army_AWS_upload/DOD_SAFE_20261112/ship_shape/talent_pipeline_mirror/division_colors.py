import matplotlib.pyplot as plt

# Example division names
divisions = [
    "Division 1", "Division 2", "Division 3", "Division 4", "Division 5",
    "Division 6", "Division 7", "Division 8", "Division 9", "Division 10"
]

# Choose a color palette (e.g., tab10, Set3, or your own)
colors = plt.get_cmap('tab10').colors  # tab10 has 10 distinct colors

# Create the mapping
division_colors = {div: colors[i] for i, div in enumerate(divisions)}

# Usage in a plot
for div in divisions:
    plt.bar(div, 1, color=division_colors[div])
plt.show()