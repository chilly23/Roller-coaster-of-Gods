from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd

"""Create beautiful plots like your reference images"""

df = pd.read_csv("attractor_data_a3.61_b-4.24.csv")  # <-- change filename as needed

# df = df.loc[0:10000000]

a = 3.61
b = -4.24

fig, ax = plt.subplots(figsize=(10, 10), dpi=1200)
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

ax.set_axis_off()
for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_aspect('equal', adjustable='box')

styles = {
    'orange': {
        'colors': ['#FFF8E1', '#FFE082', '#FF8F00', '#E65100'],
        'alpha_range': (0.1, 0.8),
        'point_size': 0.5
    },
    'red': {
        'colors': ['#FFEBEE', '#FFCDD2', '#E57373', '#C62828', '#8B0000'],
        'alpha_range': (0.05, 0.6),
        'point_size': 0.3
    },
    'pink': {
        'colors': ['#FCE4EC', '#F8BBD9', '#E91E63', '#AD1457'],
        'alpha_range': (0.1, 0.7),
        'point_size': 0.4
    },
    'blue': {
        'colors': ['#E3F2FD', '#90CAF9', '#2196F3', '#0D47A1'],
        'alpha_range': (0.1, 0.8),
        'point_size': 0.5
    }
}

style = styles['blue']

# if abs(a) > 3:
#     style = styles['red']
# elif a * b > 0:
#     style = styles['orange'] 
# elif a * b < -5:
#     style = styles['pink']
# else:
#     style = styles['blue']

custom_cmap = LinearSegmentedColormap.from_list("custom", style['colors'])
colors = np.arange(len(df['x']))
n_points = len(df['x'])
segment_size = max(1, n_points // 3000)

for i in range(0, n_points, segment_size):
    end_idx = min(i + segment_size, n_points)
    segment_x = df['x'][i:end_idx]
    segment_y = df['y'][i:end_idx]
    segment_colors = colors[i:end_idx]
    
    alpha = style['alpha_range'][0] + (style['alpha_range'][1] - style['alpha_range'][0]) * (i / n_points)
    size = style['point_size'] * (0.5 + 0.5 * (i / n_points))
    
    ax.scatter(segment_x, segment_y, 
                c=segment_colors, 
                cmap=custom_cmap,
                s=size, 
                alpha=alpha,
                edgecolors='none',
                rasterized=True)

ax.text(0.02, 0.02, f'a = {a:.2f}, b = {b:.2f}', 
        transform=ax.transAxes, fontsize=12, 
        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))

margin = 0.1
x_range = df['x'].max() - df['x'].min()
y_range = df['y'].max() - df['y'].min()
ax.set_xlim(df['x'].min() - margin * x_range, df['x'].max() + margin * x_range)
ax.set_ylim(df['y'].min() - margin * y_range, df['y'].max() + margin * y_range)

plt.tight_layout()
filename = f"attractor_a{a:.2f}_b{b:.2f}.png"
plt.savefig(filename, dpi=300, bbox_inches='tight', 
                    facecolor='white', edgecolor='none')
print(f"Saved plot as {filename}")
plt.show()
    
