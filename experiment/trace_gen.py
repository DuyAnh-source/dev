import csv
import math
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, "trajectory.csv")
def generate_circle_trajectory(center_x=-2.0, center_y=0.0, radius=2.0, z=1.5,T=20):
    
    num_points = 20 * T #T: chu kỳ 
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y', 'z'])  # header

        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            writer.writerow([round(x, 2), round(y, 2), z])

    print(f"✅ Đã tạo quỹ đạo hình tròn với {num_points} điểm trong file {filename}")

def generate_line_trajectory(start_point_x = 0.0,  start_point_y=0.0,length=50.0, z=1.5,velocity = 1.0 ):

    num_points = int (20 * length / velocity)  # Số điểm dựa trên khoảng cách và vận tốc
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y', 'z'])  # header

        for i in range(num_points):
            t =  i / num_points
            x = start_point_x + length*t
            y = start_point_y + length*t
            writer.writerow([round(x, 2), round(y, 2), z])

generate_line_trajectory()