import csv
import math

def generate_circle_trajectory(
    center_x=-2.0, center_y=0.0, radius=.0, z=1.5,
    num_points=1000, filename='trajectory.csv'
):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y', 'z'])  # header

        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            writer.writerow([x, y, z])

    print(f"✅ Đã tạo quỹ đạo hình tròn với {num_points} điểm trong file {filename}")
def generate_line_trajectory(
    center_x=0.0, center_y=0.0, radius=0.0, z=1.5,
    num_points=1000, filename='trajectory.csv'
):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y', 'z'])  # header

        for i in range(num_points):
            t =  i / num_points
            x = center_x + 50*t
            y = center_y + 50*t
            writer.writerow([x, y, z])

generate_line_trajectory()