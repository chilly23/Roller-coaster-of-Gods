import numpy as np
import csv
import random

csv_filename = f"coaster.csv"
n_points = 100000

x_val = [0]
y_val = [0]


repeatation_limit = 1000
rep_split = 0.5
not_repeating = 1

proceed = True

def generate():

    csvfile.flush()
    x0 = 0
    y0 = 0
    a = random.random()
    b = random.random()

    for i in range(n_points):
        x = np.sin(x_val[i]**2 - y_val[i]**2 + round(a,3))
        y = np.cos(2*x_val[i]*y_val[i] + round(b,3))

        if np.isinf(x) or np.isnan(x) or np.isinf(y) or np.isnan(y):
            break

        csv_writer.writerow([round(x,3), round(y,3)])

        x_val.append(x)
        y_val.append(y)

        
        if i % (n_points/100) == 0:
            progress = (i / n_points) * 100
            print(f"Progress: {progress:.1f}%")

        if x in x_val:
            x0 +=1 
        if y in y_val:
            y0 +=1

        if x0 > repeatation_limit or y0 > repeatation_limit:
            proceed = True

            print("-"*40)
            print(f"Repetitive coefficients for {round(a,3),round(b,3)}\n")
            generate()
            return 0
        else:
            if i > n_points*rep_split and not_repeating == 1:
                proceed = False
                not_repeating = 0
                print("Non repetive points found")
                print("a = ",round(a,3)," b = ",round(b,3))
                
                if i == n_points-2:
                    print("Non repetive points found")
                    print("a = ",round(a,3)," b = ",round(b,3))

with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['x', 'y'])

    generate()



#     fig, ax = plt.subplots(figsize=(15, 15))
#     fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
#     fig.set_facecolor(style["background"])
#     ax.set_axis_off()
#     ax.spines["top"].set_visible(False)
#     ax.spines["right"].set_visible(False)
#     ax.spines["left"].set_visible(False)
#     ax.spines["bottom"].set_visible(False)
#     ax.set_aspect("equal", "box")
    
#     if style["colormap"]:
#         colors = np.arange(len(points))
#         scatter = ax.scatter(points[:, 0], points[:, 1], 
#                            s=style["size"], 
#                            alpha=style["alpha"], 
#                            c=colors, 
#                            cmap=style["colormap"])
#     else:
#         ax.scatter(points[:, 0], points[:, 1], 
#                   s=style["size"], 
#                   alpha=style["alpha"], 
#                   c=style["color"])
    
#     plot_filename = f"fractal_{style_name}_x{a}_y{b}.png"
#     plt.savefig(plot_filename, dpi=300, bbox_inches='tight', 
#                 facecolor=style["background"], edgecolor='none')
#     print(f"Plot saved as {plot_filename}")
#     print(f"Data saved as {csv_filename}")
    
#     plt.show()
#     return points

# if __name__ == "__main__":
#     starting_points = [
#         (0.05, 0.05, "style1"),    # Red spiral style
#         (0.1, 0.3, "style2"),      # Plasma colormap style  
#         (-0.2, 0.1, "style3"),     # Viridis on white background
#         (0.5, -0.1, "default"),    # Original orange style
#         (3.69, 4.51, "yellow"), # yellow with white bg
#         (2.55, 0.93, "purple"), # purple with white bg
#         (2.7, 2.32, "red"), # red with white bg
#         (3.61, 4.24, "brown"), # brown with white bg
#         (0.29, 4, "orange"), # orange with white bg
#         (5.9, 5.64, "red") # red with white bg
        
#     ]
    
#     print("Choose a style to generate:")
#     print("1. Generate all styles")
#     print("2. Generate single style with custom starting point")
    
#     choice = input("Enter choice (1 or 2): ").strip()
    
#     if choice == "1":
#         for a, b, style_name in starting_points:
#             generate(a, b, style_name)
#             print("-" * 50)
    
#     elif choice == "2":
#         try:
#             a = float(input("Enter starting X coordinate: "))
#             b = float(input("Enter starting Y coordinate: "))
#             style_name = input("Enter style name (style1/style2/style3/default): ").strip()
#             if style_name not in ["style1", "style2", "style3", "default"]:
#                 style_name = "default"
            
#             n_points = int(input("Enter number of iterations (default 500000): ") or "500000")
            
#             generate(a, b, style_name, n_points)
            
#         except ValueError:
#             print("Invalid input. Using default values.")
#             generate(0.05, 0.05, "default")
    
#     else:
#         print("Invalid choice. Generating default fractal.")
#         generate(0.05, 0.05, "default")