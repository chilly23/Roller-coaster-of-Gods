import matplotlib.pyplot as plt
import numpy as np
import csv
from matplotlib.colors import LinearSegmentedColormap

def clifford_attractor(a, b, c, d, x0=0, y0=0, n_points=10000000):
    """Generate Clifford attractor points"""
    x, y = np.zeros(n_points), np.zeros(n_points)
    x[0], y[0] = x0, y0
    
    for i in range(1, n_points):
        x_new = np.sin(a * y[i-1]) + c * np.cos(a * x[i-1])
        y_new = np.sin(b * x[i-1]) + d * np.cos(b * y[i-1])
        x[i], y[i] = x_new, y_new
    
    return x, y

def dejong_attractor(a, b, c, d, x0=0, y0=0, n_points=10000000):
    """Generate De Jong attractor points"""
    x, y = np.zeros(n_points), np.zeros(n_points)
    x[0], y[0] = x0, y0
    
    for i in range(1, n_points):
        x_new = np.sin(a * y[i-1]) - np.cos(b * x[i-1])
        y_new = np.sin(c * x[i-1]) - np.cos(d * y[i-1])
        x[i], y[i] = x_new, y_new
    
    return x, y

def svensson_attractor(a, b, c, d, x0=0, y0=0, n_points=10000000):
    """Generate Svensson attractor points"""
    x, y = np.zeros(n_points), np.zeros(n_points)
    x[0], y[0] = x0, y0
    
    for i in range(1, n_points):
        x_new = d * np.sin(a * x[i-1]) - np.sin(b * y[i-1])
        y_new = c * np.cos(a * x[i-1]) + np.cos(b * y[i-1])
        x[i], y[i] = x_new, y_new
    
    return x, y

def generate_fractal(attractor_type="clifford", params=None, style_name="default", n_points=10000000, skip_points=1000):
    """Generate fractal attractor with various styles"""
    
    # Default parameters for different attractors
    default_params = {
        "clifford": [
            (-1.4, 1.6, 1.0, 0.7),    # Purple spiral
            (-2.0, -2.0, -1.2, 2.0),  # Complex pattern
            (1.7, 1.7, 0.6, 1.2),     # Circular pattern
            (-1.8, -2.0, -0.5, -0.9), # Dense spiral
            (1.5, -1.8, 1.6, 0.9),    # Flowing pattern
        ],
        "dejong": [
            (2.01, -2.53, 1.61, -0.33),  # Classic De Jong
            (-2.7, -0.09, -0.86, -2.2),  # Butterfly-like
            (1.641, 1.902, 0.316, 1.525), # Symmetric
            (-2.24, 0.43, -0.65, -2.43),  # Complex web
        ],
        "svensson": [
            (1.4, 1.56, 1.4, -6.56),     # Flowing curves
            (-1.78, -1.93, -1.44, -2.33), # Dense pattern
            (1.7, 1.8, 0.0, 1.0),        # Simple curves
        ]
    }
    
    styles = {
        "purple_dream": {
            "colors": ["#000033", "#4B0082", "#9370DB", "#DDA0DD"],
            "alpha": 0.15,
            "size": 0.1,
            "background": "black"
        },
        "sunset": {
            "colors": ["#8B0000", "#FF4500", "#FFD700", "#FFF8DC"],
            "alpha": 0.12,
            "size": 0.1,
            "background": "black"
        },
        "ocean": {
            "colors": ["#000080", "#0000FF", "#00BFFF", "#87CEEB"],
            "alpha": 0.15,
            "size": 0.1,
            "background": "black"
        },
        "fire": {
            "colors": ["#8B0000", "#DC143C", "#FF6347", "#FFD700"],
            "alpha": 0.1,
            "size": 0.1,
            "background": "black"
        },
        "forest": {
            "colors": ["#013220", "#228B22", "#32CD32", "#90EE90"],
            "alpha": 0.12,
            "size": 0.1,
            "background": "black"
        },
        "monochrome": {
            "colors": ["white"],
            "alpha": 0.05,
            "size": 0.1,
            "background": "black"
        },
        "default": {
            "colors": ["#FF4500", "#FFD700"],
            "alpha": 0.1,
            "size": 0.1,
            "background": "black"
        }
    }
    
    # Use provided parameters or default ones
    if params is None:
        param_sets = default_params.get(attractor_type, default_params["clifford"])
        a, b, c, d = param_sets[0]  # Use first parameter set
    else:
        a, b, c, d = params
    
    style = styles.get(style_name, styles["default"])
    
    print(f"Generating {attractor_type} attractor with parameters: a={a}, b={b}, c={c}, d={d}")
    
    # Generate points based on attractor type
    if attractor_type == "clifford":
        x, y = clifford_attractor(a, b, c, d, n_points=n_points)
    elif attractor_type == "dejong":
        x, y = dejong_attractor(a, b, c, d, n_points=n_points)
    elif attractor_type == "svensson":
        x, y = svensson_attractor(a, b, c, d, n_points=n_points)
    else:
        print("Unknown attractor type, using Clifford")
        x, y = clifford_attractor(a, b, c, d, n_points=n_points)
    
    # Skip initial points to avoid transient behavior
    x = x[skip_points:]
    y = y[skip_points:]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor(style["background"])
    ax.set_facecolor(style["background"])
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Create custom colormap if multiple colors
    if len(style["colors"]) > 1:
        cmap = LinearSegmentedColormap.from_list("custom", style["colors"])
        colors = np.linspace(0, 1, len(x))
        scatter = ax.scatter(x, y, s=style["size"], alpha=style["alpha"], 
                           c=colors, cmap=cmap, rasterized=True)
    else:
        ax.scatter(x, y, s=style["size"], alpha=style["alpha"], 
                  c=style["colors"][0], rasterized=True)
    
    # Remove margins
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    
    # Save files
    filename_base = f"{attractor_type}_{style_name}_a{a}_b{b}_c{c}_d{d}"
    plot_filename = f"{filename_base}.png"
    csv_filename = f"{filename_base}.csv"
    
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight', 
                facecolor=style["background"], edgecolor='none', pad_inches=0)
    print(f"Plot saved as {plot_filename}")
    
    # Save to CSV
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x', 'y'])
        for i in range(0, len(x), 100):  # Save every 100th point to reduce file size
            writer.writerow([round(float(x[i]), 6), round(float(y[i]), 6)])
    print(f"Data saved as {csv_filename}")
    
    plt.show()
    return x, y

# Predefined beautiful parameter sets
beautiful_sets = {
    "clifford": [
        (-1.4, 1.6, 1.0, 0.7, "purple_dream"),    # Purple spiral like image 1
        (-2.0, -2.0, -1.2, 2.0, "sunset"),        # Orange/red pattern like image 2  
        (1.7, 1.7, 0.6, 1.2, "ocean"),           # Blue circular pattern
        (-1.8, -2.0, -0.5, -0.9, "fire"),        # Red/pink dense spiral like image 5
        (1.5, -1.8, 1.6, 0.9, "forest"),         # Green flowing pattern
    ],
    "dejong": [
        (2.01, -2.53, 1.61, -0.33, "purple_dream"), # Classic beautiful pattern
        (-2.7, -0.09, -0.86, -2.2, "sunset"),       # Butterfly-like
        (1.641, 1.902, 0.316, 1.525, "fire"),       # Symmetric red pattern
    ]
}

if __name__ == "__main__":
    print("Fractal Attractor Generator")
    print("=" * 40)
    print("1. Generate beautiful preset fractals")
    print("2. Generate custom fractal")
    print("3. Generate all presets")
    
    choice = input("\nEnter choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        print("\nAvailable presets:")
        all_presets = []
        idx = 1
        for attractor_type, param_list in beautiful_sets.items():
            for params in param_list:
                a, b, c, d, style = params
                print(f"{idx}. {attractor_type.title()} - {style} (a={a}, b={b}, c={c}, d={d})")
                all_presets.append((attractor_type, params))
                idx += 1
        
        try:
            preset_choice = int(input(f"\nChoose preset (1-{len(all_presets)}): ")) - 1
            if 0 <= preset_choice < len(all_presets):
                attractor_type, params = all_presets[preset_choice]
                a, b, c, d, style = params
                generate_fractal(attractor_type, (a, b, c, d), style)
            else:
                print("Invalid choice, using default")
                generate_fractal()
        except ValueError:
            print("Invalid input, using default")
            generate_fractal()
    
    elif choice == "2":
        try:
            attractor_type = input("Attractor type (clifford/dejong/svensson): ").lower()
            if attractor_type not in ["clifford", "dejong", "svensson"]:
                attractor_type = "clifford"
            
            a = float(input("Parameter a: "))
            b = float(input("Parameter b: "))
            c = float(input("Parameter c: "))
            d = float(input("Parameter d: "))
            
            style = input("Style (purple_dream/sunset/ocean/fire/forest/monochrome/default): ")
            if style not in ["purple_dream", "sunset", "ocean", "fire", "forest", "monochrome", "default"]:
                style = "default"
            
            n_points = int(input("Number of points (default 1000000): ") or "1000000")
            
            generate_fractal(attractor_type, (a, b, c, d), style, n_points)
            
        except ValueError:
            print("Invalid input, using default parameters")
            generate_fractal()
    
    elif choice == "3":
        print("Generating all preset fractals...")
        for attractor_type, param_list in beautiful_sets.items():
            for params in param_list:
                a, b, c, d, style = params
                print(f"\nGenerating {attractor_type} with style {style}...")
                generate_fractal(attractor_type, (a, b, c, d), style)
                print("-" * 50)
    
    else:
        print("Invalid choice, generating default fractal")
        generate_fractal()