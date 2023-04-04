import airsim

# 连接到AirSim客户端
client = airsim.MultirotorClient()

# 确保与仿真器的连接
client.confirmConnection()
client.enableApiControl(True)   # 获取控制权

# 启用（arm）无人机的电机
client.armDisarm(True)

# 使无人机起飞
client.takeoffAsync().join()

# 在此处执行你的任务，例如移动无人机、拍照等

# 使无人机降落
# client.landAsync().join()
#
# 禁用（disarm）无人机的电机
# client.armDisarm(False)
