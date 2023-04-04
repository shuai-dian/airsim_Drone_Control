"""
飞正方形（速度控制）
"""
import airsim
import time
client = airsim.MultirotorClient()  # connect to the AirSim simulator
client.enableApiControl(True)       # 获取控制权
client.armDisarm(True)              # 解锁

landed = client.getMultirotorState().landed_state
if landed == airsim.LandedState.Landed:
    print("taking off...")
    client.takeoffAsync().join()

client.moveToZAsync(-5, 1).join()   # 第二阶段：上升到2米高度

# 飞正方形
client.moveByVelocityZAsync(5, 0, -2, 8).join()     # 第三阶段：以1m/s速度向前飞8秒钟
# client.moveByVelocityZAsync(0, 1, -2, 8).join()     # 第三阶段：以1m/s速度向右飞8秒钟
# client.moveByVelocityZAsync(-1, 0, -2, 8).join()    # 第三阶段：以1m/s速度向后飞8秒钟
# client.moveByVelocityZAsync(0, -1, -2, 8).join()    # 第三阶段：以1m/s速度向左飞8秒钟

# 悬停 2 秒钟
client.hoverAsync().join()          # 第四阶段：悬停6秒钟
# time.sleep(6)
# client.landAsync().join()           # 第五阶段：降落
# client.armDisarm(False)             # 上锁
# client.enableApiControl(False)      # 释放控制权