from pyulog import ULog
import pandas as pd

# Thay đổi đường dẫn file ULog của bạn
import ulogfile as ulogfile 
ulog =ulogfile.get_ulog()

# Lấy tất cả các message liên quan đến GPS
gps_data = None
for d in ulog.data_list:
    if d.name == 'vehicle_gps_position':
        gps_data = d
        break

if gps_data is None:
    print("Không tìm thấy dữ liệu GPS trong ULog!")
    exit()

# Chuyển dữ liệu GPS thành dataframe
df = pd.DataFrame.from_dict(gps_data.data)
print(df.columns)
# PX4 lưu tọa độ ở dạng nguyên (int), cần chia cho 1e7 để ra giá trị thực
df['latitude_deg'] = df['latitude_deg'] 
df['longitude_deg'] = df['longitude_deg'] 
df['altitude_msl_m'] = df['altitude_msl_m']  # Đơn vị thường là mm => m

# In ra một số dòng đầu tiên
print(df[['timestamp', 'latitude_deg', 'longitude_deg', 'altitude_msl_m']].head())

# Lưu ra file csv nếu cần
