import matplotlib.pyplot as plt
import numpy as np


def plot_average_ratings(item_names, average_ratings):
  # Set up figure with crisp resolution
  _, ax = plt.subplots(figsize=(11, 6), dpi=120)

  # Generate rainbow colors mapped across all items
  colors = plt.cm.rainbow(np.linspace(0.1, 0.9, len(item_names)))

  # Plot bars with subtle outline and zorder to stay above gridlines
  bars = ax.bar(
    item_names, 
    average_ratings, 
    color=colors, 
    edgecolor='#333333', 
    linewidth=0.8, 
    width=0.6, 
    zorder=3
  )

  # Titles and Labels
  ax.set_title("Average Rating of Each Book", fontsize=16, fontweight='bold', pad=15, color='#2c3e50')
  ax.set_xlabel("Books", fontsize=12, fontweight='bold', labelpad=10, color='#2c3e50')
  ax.set_ylabel("Average Rating (0 – 5)", fontsize=12, fontweight='bold', labelpad=10, color='#2c3e50')

  # Y-axis range (slightly expanded to fit value labels comfortably)
  ax.set_ylim(0, 5.5)

  # Rotate tick labels and style them
  ax.set_xticks(range(len(item_names)))
  ax.set_xticklabels(item_names, rotation=45, ha="right", fontsize=10, color='#333333')
  ax.tick_params(axis='y', labelsize=10)

  # Add numeric labels on top of each bar
  ax.bar_label(bars, fmt='%.2f', padding=4, fontsize=9, fontweight='bold', color='#2c3e50')

  # Add horizontal gridlines behind the bars
  ax.grid(axis='y', linestyle='--', alpha=0.6, zorder=0)

  # Clean borders (remove top and right spines)
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['left'].set_color('#888888')
  ax.spines['bottom'].set_color('#888888')

  plt.tight_layout()
  plt.show()