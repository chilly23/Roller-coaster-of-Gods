import numpy as np
import csv
import random
import coasterplot

def generate_fractal():
    csv_filename = "coaster.csv"
    n_points = 100000
    repetition_limit = 100000
    rep_split = 0.5
    tolerance = 1e-6  # For floating point comparison
    
    max_attempts = 100  # Prevent infinite loops
    
    for attempt in range(max_attempts):
        print(f"\nAttempt {attempt + 1}/{max_attempts}")
        
        # Generate random coefficients for Clifford Attractor
        # Standard range is -3 to +3, but we'll use -2 to +2 for stability
        a = random.uniform(-2.0, 2.0)
        b = random.uniform(-2.0, 2.0) 
        c = random.uniform(-2.0, 2.0)
        d = random.uniform(-2.0, 2.0)
        print(f"Testing coefficients: a={round(a,3)}, b={round(b,3)}, c={round(c,3)}, d={round(d,3)}")
        
        # Initialize starting values
        x_val = [0.0]
        y_val = [0.0]
        
        # Counters for repetition detection
        repetition_count = 0
        is_valid_sequence = True
        
        # Open CSV file for this attempt
        with open(csv_filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['x', 'y'])
            
            # Write initial point
            csv_writer.writerow([0.0, 0.0])
            
            for i in range(1, n_points):
                # Clifford Attractor equations
                x = np.sin(a * y_val[i-1]) + c * np.cos(a * x_val[i-1])
                y = np.sin(b * x_val[i-1]) + d * np.cos(b * y_val[i-1])
                
                # Check for invalid values (inf, nan)
                if np.isinf(x) or np.isnan(x) or np.isinf(y) or np.isnan(y):
                    print(f"Invalid values encountered at iteration {i}")
                    is_valid_sequence = False
                    break
                
                # Check for repetition (with tolerance for floating point comparison)
                is_repetitive = False
                for j in range(len(x_val)):
                    if (abs(x - x_val[j]) < tolerance and abs(y - y_val[j]) < tolerance):
                        repetition_count += 1
                        is_repetitive = True
                        break
                
                # If too many repetitions found early, abandon this attempt
                if repetition_count > repetition_limit and i < n_points * rep_split:
                    print(f"Too many repetitions ({repetition_count}) found early at iteration {i}")
                    is_valid_sequence = False
                    break
                
                # Add the new point
                x_val.append(round(x, 6))  # Round to avoid floating point precision issues
                y_val.append(round(y, 6))
                csv_writer.writerow([round(x, 3), round(y, 3)])
                
                # Progress reporting
                if i % (n_points // 100) == 0:
                    progress = (i / n_points) * 100
                    print(f"Progress: {progress:.1f}% - Repetitions so far: {repetition_count}")
                
                # Flush periodically to save progress
                if i % 10000 == 0:
                    csvfile.flush()
            
            # Check if we completed successfully
            if is_valid_sequence and i >= n_points * rep_split:
                final_repetition_rate = (repetition_count / len(x_val)) * 100
                print("-" * 50)
                print("SUCCESS: Non-repetitive sequence found!")
                print(f"Final coefficients: a={round(a,3)}, b={round(b,3)}, c={round(c,3)}, d={round(d,3)}")
                print(f"Points generated: {len(x_val)}")
                print(f"Total repetitions: {repetition_count}")
                print(f"Repetition rate: {final_repetition_rate:.2f}%")
                print(f"Data saved to: {csv_filename}")
                coasterplot.coasterplot(csv_filename)
                return a, b, c, d, x_val, y_val
            
            print(f"Attempt {attempt + 1} failed - trying new coefficients...")
    
    print("Maximum attempts reached. Could not find suitable coefficients.")
    return None, None, None, None, None, None

def plot_fractal(x_val, y_val, a, b, c, d):
    """Optional plotting function - uncomment matplotlib imports to use"""
    try:
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(12, 12))
        fig.set_facecolor('black')
        ax.set_facecolor('black')
        ax.set_axis_off()
        ax.set_aspect("equal", "box")
        
        # Create colormap based on point order
        colors = np.arange(len(x_val))
        scatter = ax.scatter(x_val, y_val, 
                           s=0.1, 
                           alpha=0.7, 
                           c=colors, 
                           cmap='plasma')
        
        plot_filename = f"fractal_a{round(a,3)}_b{round(b,3)}.png"
        plt.savefig(plot_filename, dpi=300, bbox_inches='tight', 
                    facecolor='black', edgecolor='none')
        print(f"Plot saved as {plot_filename}")
        plt.show()
        
    except ImportError:
        print("Matplotlib not available for plotting")

if __name__ == "__main__":
    print("Starting fractal generation...")
    a, b, x_points, y_points = generate_fractal()
    
    if a is not None:
        # Uncomment the next line if you want to plot the results
        # plot_fractal(x_points, y_points, a, b)
        print("\nFractal generation completed successfully!")
    else:
        print("\nFractal generation failed after all attempts.")