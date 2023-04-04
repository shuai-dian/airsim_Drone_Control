import airsim
import time
from math import sin, cos, sqrt, asin, radians

def print_state():
    print("===============================================================")
    state = client.getMultirotorState()
    print(state)

# 根据经纬度 求 两点之间的距离
def get_p_t_p_distance(lng1, lat1, lng2, lat2):
    # lng1,lat1,lng2,lat2 = (120.12802999999997,30.28708,115.86572000000001,28.7427)
    lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)])  # 经纬度转换成弧度
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    distance = 2 * asin(sqrt(a)) * 6371 * 1000  # 地球平均半径，6371km
    # distance = round(distance / 1000, 3)
    return distance

# lng1, lat1, lng2, lat2 = ( -122.14016495104394,47.64146796210233, -122.14016495104089, 47.64189285169751)
print(get_p_t_p_distance(-122.14016495104394,47.64146796210233, -122.14016495117276,47.64310934308369))
# 返回 446.721 千米



client = airsim.MultirotorClient()  # connect to the AirSim simulator
client.enableApiControl(True)       # 获取控制权
client.armDisarm(True)              # 解锁
client.takeoffAsync().join()        # 第一阶段：起飞
client.moveToZAsync(-30, 1).join()   # 第二阶段：上升到2米高度

# 飞正方形
client.moveByVelocityZAsync(8, 0, -30, 30).join()     # 第三阶段：以8m/s速度向前飞2秒钟  # 80
client.hoverAsync().join()          # 第四阶段：悬停6秒钟
print_state()
client.moveByVelocityZAsync(0, -8, -30, 30).join()    # 第三阶段：以8m/s速度向左飞2秒钟
client.hoverAsync().join()          # 第四阶段：悬停6秒钟
print_state()
client.moveByVelocityZAsync(-8, 0, -30, 30).join()    # 第三阶段：以8m/s速度向后飞2秒钟
client.hoverAsync().join()          # 第四阶段：悬停6秒钟
print_state()
client.moveByVelocityZAsync(0, 8, -30, 30).join()     # 第三阶段：以8m/s速度向右飞2秒钟
client.hoverAsync().join()          # 第四阶段：悬停6秒钟
print_state()

# 悬停 2 秒钟
client.hoverAsync().join()          # 第四阶段：悬停6秒钟
time.sleep(6)
client.landAsync().join()           # 第五阶段：降落
client.armDisarm(False)             # 上锁
client.enableApiControl(False)      # 释放控制权
