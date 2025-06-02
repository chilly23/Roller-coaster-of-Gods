import serial
import csv

csv_filename = "coaster_v1.csv"
vals = 0
max_vals = 1000000

import time
ser = serial.Serial("COM5", 115200)
time.sleep(2)  # Wait for Arduino to reset
ser.write(b"START\n")


with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['x', 'y'])

    print(f"Listening on {ser.name}... Writing to {csv_filename}")
    
    while True:
        try:
            line = ser.readline().decode().strip()

            if line in ["START", "DONE", "STOP"]:
                print(f"[ARDUINO] {line}")
                if line in ["DONE", "STOP"]:
                    break
                continue

            x, y = map(float, line.split(","))
            csv_writer.writerow([round(x, 3), round(y, 3)])
            vals += 1

            if vals % 10000 == 0:
                print(f"Saved {vals} points...")

            if vals >= max_vals:
                print("Reached max point limit.")
                break

        except Exception as e:
            # Skip malformed lines
            continue

print(f"Finished saving {vals} points to {csv_filename}")
