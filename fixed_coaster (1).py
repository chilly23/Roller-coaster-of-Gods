import numpy as np
import csv
import random
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def generate_fractal_attractor(a, b, n_points=5000000, max_iterations_check=100000):
    """Generate fractal attractor using modified equations"""
    
    # Initialize arrays
    x_vals = [0.0]
    y_vals = [0.0]
    
    # Track if the system escapes to infinity or gets stuck
    for i in range(1, n_points):
        x_prev = x_vals[i-1]
        y_prev = y_vals[i-1]
        
        # Your original style equations (they actually work well for attractors!)
        x_new = np.sin(x_prev*x_prev - y_prev*y_prev + a)
        y_new = np.cos(2*x_prev*y_prev + b)
        
        # Check for invalid values
        if np.isinf(x_new) or np.isnan(x_new) or np.isinf(y_new) or np.isnan(y_new):
            print(f"System diverged at iteration {i}")
            break
            
        # Check if system is exploding (values too large)
        if abs(x_new) > 100 or abs(y_new) > 100:
            print(f"System escaped to infinity at iteration {i}")
            break
            
        x_vals.append(x_new)
        y_vals.append(y_new)
        
        # Early check for boring attractors (stuck at fixed point)
        if i > max_iterations_check:
            recent_x = x_vals[-1000:]
            recent_y = y_vals[-1000:]
            if (max(recent_x) - min(recent_x) < 0.001 and 
                max(recent_y) - min(recent_y) < 0.001):
                print(f"System converged to fixed point")
                return None, None
    
    return np.array(x_vals), np.array(y_vals)

def create_beautiful_plot(x_vals, y_vals, a, b, style_name="default"):
    """Create beautiful plots like your reference images"""
    
    # Create figure with high DPI for quality
    fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Remove axes and spines for clean look
    ax.set_axis_off()
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Set equal aspect ratio
    ax.set_aspect('equal', adjustable='box')
    
    # Define different color styles
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
    
    # Choose style based on parameter values or randomly
    if abs(a) > 3:
        style = styles['red']
    elif a * b > 0:
        style = styles['orange'] 
    elif a * b < -5:
        style = styles['pink']
    else:
        style = styles['blue']
    
    # Create custom colormap
    custom_cmap = LinearSegmentedColormap.from_list("custom", style['colors'])
    
    # Create color array based on iteration (creates the flowing effect)
    colors = np.arange(len(x_vals))
    
    # Plot the attractor with varying alpha and size for depth effect
    n_points = len(x_vals)
    
    # Plot in segments for gradient effect
    segment_size = max(1, n_points // 1000)
    
    for i in range(0, n_points, segment_size):
        end_idx = min(i + segment_size, n_points)
        segment_x = x_vals[i:end_idx]
        segment_y = y_vals[i:end_idx]
        segment_colors = colors[i:end_idx]
        
        # Vary alpha and size based on position in sequence
        alpha = style['alpha_range'][0] + (style['alpha_range'][1] - style['alpha_range'][0]) * (i / n_points)
        size = style['point_size'] * (0.5 + 0.5 * (i / n_points))
        
        ax.scatter(segment_x, segment_y, 
                  c=segment_colors, 
                  cmap=custom_cmap,
                  s=size, 
                  alpha=alpha,
                  edgecolors='none',
                  rasterized=True)
    
    # Set title with parameters
    ax.text(0.02, 0.02, f'a = {a:.2f}, b = {b:.2f}', 
            transform=ax.transAxes, fontsize=12, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # Adjust margins to fit the entire attractor
    margin = 0.1
    x_range = x_vals.max() - x_vals.min()
    y_range = y_vals.max() - y_vals.min()
    ax.set_xlim(x_vals.min() - margin * x_range, x_vals.max() + margin * x_range)
    ax.set_ylim(y_vals.min() - margin * y_range, y_vals.max() + margin * y_range)
    
    plt.tight_layout()
    return fig, ax

def find_interesting_attractors(num_attempts=50):
    """Find interesting attractor parameters"""
    
    # Some known good parameter ranges based on your examples
    interesting_params = []
    
    print("Searching for interesting attractors...")
    
    for attempt in range(num_attempts):
        # Generate parameters in ranges that tend to produce interesting results
        a = random.uniform(-6, 6)
        b = random.uniform(-6, 6)
        
        print(f"Testing a={a:.3f}, b={b:.3f} ({attempt+1}/{num_attempts})")
        
        # Generate the attractor
        x_vals, y_vals = generate_fractal_attractor(a, b, n_points=500000)
        
        if x_vals is not None and len(x_vals) > 10000:
            # Check if it's interesting (good spread, not too chaotic)
            x_range = x_vals.max() - x_vals.min()
            y_range = y_vals.max() - y_vals.min()
            
            if (0.5 < x_range < 20 and 0.5 < y_range < 20 and 
                len(x_vals) > 20000):
                interesting_params.append((a, b, len(x_vals)))
                print(f"  ✓ Found interesting attractor! Range: {x_range:.2f} x {y_range:.2f}")
    
    return interesting_params

def main():
    # First, let's try some parameters that should work well
    test_params = [
        (3.69, 4.51),
        (3.61, -4.24),
        (0.29, 4.0),
        (5.92, -2.89)
    ]
    
    print("Generating attractors with known good parameters...")
    
    for i, (a, b) in enumerate(test_params):
        print(f"\nGenerating attractor {i+1}: a={a}, b={b}")
        
        # Generate full resolution attractor
        x_vals, y_vals = generate_fractal_attractor(a, b, n_points=5000000)
        
        if x_vals is not None:
            print(f"Generated {len(x_vals)} points")
            
            # Create and save plot
            fig, ax = create_beautiful_plot(x_vals, y_vals, a, b)
            
            filename = f"attractor_a{a:.2f}_b{b:.2f}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            print(f"Saved plot as {filename}")
            
            # Save data to CSV
            csv_filename = f"attractor_data_a{a:.2f}_b{b:.2f}.csv"
            with open(csv_filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['x', 'y'])
                for x, y in zip(x_vals, y_vals):
                    writer.writerow([f"{x:.6f}", f"{y:.6f}"])
            print(f"Saved data as {csv_filename}")
            
            plt.show()
        else:
            print("Failed to generate stable attractor")
    
    # Optionally search for new interesting parameters
    search_new = input("\nSearch for new interesting parameters? (y/n): ").lower().strip()
    if search_new == 'y':
        interesting = find_interesting_attractors(20)
        if interesting:
            print(f"\nFound {len(interesting)} interesting parameter sets:")
            for a, b, points in interesting:
                print(f"  a={a:.3f}, b={b:.3f} ({points} points)")

if __name__ == "__main__":
    main()
