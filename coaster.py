import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

def list2f(ifs):
    """From a list of x and y arrays coefficients to f1 and f2"""
    it1 = ifs[0]
    it2 = ifs[1]

    def f1(x, y):
        return (
            it1[0]
            + it1[1] * x
            + it1[2] * x**2
            + it1[3] * x * y
            + it1[4] * y
            + it1[5] * y**2
        )

    def f2(x, y):
        return (
            it2[0]
            + it2[1] * x
            + it2[2] * x**2
            + it2[3] * x * y
            + it2[4] * y
            + it2[5] * y**2
        )

    return f1, f2

def generate(start_x, start_y, style_name="default", n_points=10000000):
    ifs = [
        np.array([-0.28752426, 0.65608465, 0.71259527, 1.34370624, 1.01724109, 0.19113889]),
        np.array([-1.06839961, 0.29822047, 0.35672293, -0.68326573, 0.68020521, 1.18480771]),
    ]
    
    styles = {
        "style1": {
            "color": "red",
            "alpha": 0.1,
            "size": 0.001,
            "background": "black",
            "colormap": None
        },
        "style2": {
            "color": None,
            "alpha": 0.2,
            "size": 0.001,
            "background": "black",
            "colormap": "plasma"
        },
        "style3": {
            "color": None,
            "alpha": 0.15,
            "size": 0.001,
            "background": "white",
            "colormap": "viridis"
        },
        "yellow": {
            "color": "yellow",
            "alpha": 0.15,
            "size": 0.001,
            "background": "white",
            "colormap": "none"
        },
        "purple": {
            "color": "purple",
            "alpha": 0.15,
            "size": 0.001,
            "background": "white",
            "colormap": "none"
        },
        "brown": {
            "color": "brown",
            "alpha": 0.15,
            "size": 0.001,
            "background": "white",
            "colormap": "none"
        },
        "red": {
            "color": "red",
            "alpha": 0.15,
            "size": 0.001,
            "background": "white",
            "colormap": "none"
        },
        "orange": {
            "color": "orange",
            "alpha": 0.15,
            "size": 0.001,
            "background": "white",
            "colormap": "none"
        },
        "default": {
            "color": "orange",
            "alpha": 0.3,
            "size": 0.001,
            "background": "lightgray",
            "colormap": None
        }
    }
    
    style = styles.get(style_name, styles["default"])
    
    csv_filename = f"coaster_{style_name}_x{start_x}_y{start_y}.csv"
    
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['x', 'y'])

        fx, fy = list2f(ifs)
        points = np.zeros((n_points, 2))
        x, y = start_x, start_y
        points[0, 0], points[0, 1] = x, y
        
        print(f"Generating {style_name} fractal with starting point ({start_x}, {start_y})...")
        
        for i in range(1, n_points):
            if i % (n_points/100) == 0:
                progress = (i / n_points) * 100
                print(f"Progress: {progress:.1f}%")
            
    
            x_new, y_new = fx(x, y), fy(x, y)

            if np.isinf(x_new) or np.isnan(x_new) or np.isinf(y_new) or np.isnan(y_new):
                break

            x, y = np.clip(x_new, -1e4, 1e4), np.clip(y_new, -1e4, 1e4)
            points[i] = [x, y]
            csv_writer.writerow([round(x, 3), round(y, 3)])


    fig, ax = plt.subplots(figsize=(15, 15))
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
    fig.set_facecolor(style["background"])
    ax.set_axis_off()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_aspect("equal", "box")
    
    if style["colormap"]:
        colors = np.arange(len(points))
        scatter = ax.scatter(points[:, 0], points[:, 1], 
                           s=style["size"], 
                           alpha=style["alpha"], 
                           c=colors, 
                           cmap=style["colormap"])
    else:
        ax.scatter(points[:, 0], points[:, 1], 
                  s=style["size"], 
                  alpha=style["alpha"], 
                  c=style["color"])
    
    plot_filename = f"fractal_{style_name}_x{start_x}_y{start_y}.png"
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight', 
                facecolor=style["background"], edgecolor='none')
    print(f"Plot saved as {plot_filename}")
    print(f"Data saved as {csv_filename}")
    
    plt.show()
    return points

if __name__ == "__main__":
    starting_points = [
        (0.05, 0.05, "style1"),    # Red spiral style
        (0.1, 0.3, "style2"),      # Plasma colormap style  
        (-0.2, 0.1, "style3"),     # Viridis on white background
        (0.5, -0.1, "default"),    # Original orange style
        (3.69, 4.51, "yellow"), # yellow with white bg
        (2.55, 0.93, "purple"), # purple with white bg
        (2.7, 2.32, "red"), # red with white bg
        (3.61, 4.24, "brown"), # brown with white bg
        (0.29, 4, "orange"), # orange with white bg
        (5.9, 5.64, "red") # red with white bg
        
    ]
    
    print("Choose a style to generate:")
    print("1. Generate all styles")
    print("2. Generate single style with custom starting point")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        for start_x, start_y, style_name in starting_points:
            generate(start_x, start_y, style_name)
            print("-" * 50)
    
    elif choice == "2":
        try:
            start_x = float(input("Enter starting X coordinate: "))
            start_y = float(input("Enter starting Y coordinate: "))
            style_name = input("Enter style name (style1/style2/style3/default): ").strip()
            if style_name not in ["style1", "style2", "style3", "default"]:
                style_name = "default"
            
            n_points = int(input("Enter number of iterations (default 500000): ") or "500000")
            
            generate(start_x, start_y, style_name, n_points)
            
        except ValueError:
            print("Invalid input. Using default values.")
            generate(0.05, 0.05, "default")
    
    else:
        print("Invalid choice. Generating default fractal.")
        generate(0.05, 0.05, "default")