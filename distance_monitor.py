import serial
import math

# Haversine距離計算
def calc_distance(lat1, lon1, lat2, lon2):
    R = 6378137  # 地球の半径[m]
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad)*math.cos(lat2_rad)*math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# シリアル設定
port = "COM3"
baudrate = 115200
ser = serial.Serial(port, baudrate, timeout=1)

print("座標取得中...（数秒待ってください）")

start_lat = None
start_lon = None

# 一度現在座標を取得して確認
while True:
    line = ser.readline().decode(errors="ignore")
    if line.startswith("$GNGGA"):
        fields = line.split(",")
        if len(fields) > 5 and fields[2] and fields[4]:
            lat_raw = float(fields[2])
            lon_raw = float(fields[4])
            lat = int(lat_raw/100) + (lat_raw%100)/60
            lon = int(lon_raw/100) + (lon_raw%100)/60

            print(f"現在の座標: lat={lat:.8f}, lon={lon:.8f}")
            user_input = input("この座標を基準点にして良いですか？ (Y/N): ")
            if user_input.lower() == "y":
                start_lat = lat
                start_lon = lon
                print(f"基準点を設定しました: lat={lat:.8f}, lon={lon:.8f}")
                break
            else:
                print("もう一度座標を取得します…")
                
# しきい値入力
while True:
    try:
        threshold = float(input("ブザーを鳴らす距離[m]を入力してください: "))
        break
    except:
        print("数字を入力してください。")

print(f"{threshold}m 以上移動したら通知します。")

# メインループ
while True:
    line = ser.readline().decode(errors="ignore")
    if line.startswith("$GNGGA"):
        fields = line.split(",")
        if len(fields) > 5 and fields[2] and fields[4]:
            lat_raw = float(fields[2])
            lon_raw = float(fields[4])
            lat = int(lat_raw/100) + (lat_raw%100)/60
            lon = int(lon_raw/100) + (lon_raw%100)/60

            distance = calc_distance(start_lat, start_lon, lat, lon)
            print(f"現在 {distance:.2f} m 移動しました。")

            if distance >= threshold:
                print("ピピピ！（ブザー ON）")
