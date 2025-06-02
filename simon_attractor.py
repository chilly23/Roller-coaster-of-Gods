import numpy as np
import matplotlib.pyplot as plt

def simon_attractor(a=1.1, num_points=200000, dt=0.01):
    """
    Generate the Simon attractor (also known as Simon's attractor)
    
    The equations are:
    x_n+1 = a - x_n^2 + 0.3 * y_n
    y_n+1 = x_n
    
    This creates the beautiful flowing spiral patterns
    """
    
    # Initialize arrays
    x = np.zeros(num_points)
    y = np.zeros(num_points)
    
    # Initial conditions
    x[0], y[0] = 0.1, 0.1
    
    # Generate trajectory using the Simon map
    for i in range(1, num_points):
        x_new = a - x[i-1]**2 + 0.3 * y[i-1]
        y_new = x[i-1]
        
        x[i] = x_new
        y[i] = y_new
    
    return x, y

# Generate the attractor with parameters that create beautiful patterns
print("Generating Simon attractor...")
x, y = simon_attractor(a=1.1, num_points=150000, dt=0.01)

# Create the main 2D plot
plt.figure(figsize=(12, 10))
plt.style.use('dark_background')

# Skip transient behavior
skip = 1000
x_plot = x[skip:]
y_plot = y[skip:]

# Create gradient coloring
n_points = len(x_plot)
colors = np.linspace(0, 1, n_points)

# Plot with varying colors to show the flow
plt.scatter(x_plot[::20], y_plot[::20], c=colors[::20], 
           cmap='plasma', s=0.1, alpha=0.8)

plt.title('Simon Attractor - 2D Chaos Plot', fontsize=18, fontweight='bold', color='white')
plt.xlabel('X', fontsize=14, color='white')
plt.ylabel('Y', fontsize=14, color='white')
plt.grid(True, alpha=0.2)

# Make it look beautiful
plt.tight_layout()
plt.show()

# Create a version with different parameter for comparison
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.patch.set_facecolor('black')

parameters = [1.1, 1.3, 1.4, 1.5]
titles = ['a = 1.1', 'a = 1.3', 'a = 1.4', 'a = 1.5']

for i, (a_param, title) in enumerate(zip(parameters, titles)):
    row, col = i // 2, i % 2
    x_param, y_param = simon_attractor(a=a_param, num_points=50000)
    
    skip = 500
    axes[row, col].scatter(x_param[skip::10], y_param[skip::10], 
                          c=np.arange(len(x_param[skip::10])), 
                          cmap='plasma', s=0.2, alpha=0.8)
    axes[row, col].set_title(title, fontsize=14, color='white', fontweight='bold')
    axes[row, col].set_xlabel('X', color='white')
    axes[row, col].set_ylabel('Y', color='white')
    axes[row, col].set_facecolor('black')
    axes[row, col].grid(True, alpha=0.2)
    axes[row, col].tick_params(colors='white')

plt.suptitle('Simon Attractor - Parameter Exploration', fontsize=16, fontweight='bold', color='white')
plt.tight_layout()
plt.show()

# Create a high-resolution artistic version
plt.figure(figsize=(14, 10))
plt.style.use('dark_background')

# Generate high-resolution data
x_hires, y_hires = simon_attractor(a=1.1, num_points=300000)
skip = 2000

# Create the beautiful flowing pattern
plt.plot(x_hires[skip:], y_hires[skip:], color='cyan', alpha=0.6, linewidth=0.1)
plt.scatter(x_hires[skip::100], y_hires[skip::100], 
           c=np.arange(len(x_hires[skip::100])), 
           cmap='plasma', s=0.5, alpha=0.8)

plt.title('Simon Attractor - High Resolution Flow', fontsize=18, fontweight='bold', color='white')
plt.xlabel('X', fontsize=14, color='white')
plt.ylabel('Y', fontsize=14, color='white')
plt.grid(True, alpha=0.1)
plt.tight_layout()
plt.show()

# Print statistics
print(f"\nSimon Attractor Statistics:")
print(f"Number of points: {len(x)}")
print(f"X range: [{x[skip:].min():.3f}, {x[skip:].max():.3f}]")
print(f"Y range: [{y[skip:].min():.3f}, {y[skip:].max():.3f}]")

print("\nThe Simon attractor creates beautiful flowing spiral patterns!")
print("Try different 'a' parameter values (typically 1.0 to 1.6) for different shapes.")