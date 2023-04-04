import setup_path
import airsim

import sys
import time
import argparse


class SurveyNavigator:
    def __init__(self, args):
        self.boxsize = args.size   # 50
        self.stripewidth = args.stripewidth   # 10
        self.altitude = args.altitude     # 200  #海拔高度
        self.velocity = args.speed        # 速度   5
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()    # 每1秒检查一次连接状态，并在控制台中报告，以便用户可以查看连接的进度（实际操作只显示一次，奇怪）。
        self.client.enableApiControl(True)  # 默认是false，有的无人机不允许用API控制，所以用isApiControlEnabled可以查看是否可以用API控制   # 也就是获取虚拟遥感

    def start(self):
        print("arming the drone...")  #
        self.client.armDisarm(True)  # 解锁

        landed = self.client.getMultirotorState().landed_state
        if landed == airsim.LandedState.Landed:
            print("taking off...")
            self.client.takeoffAsync().join()

        landed = self.client.getMultirotorState().landed_state
        if landed == airsim.LandedState.Landed:
            print("takeoff failed - check Unreal message log for details")
            return

        # AirSim uses NED coordinates so negative axis is up.
        x = -self.boxsize
        z = -self.altitude

        print("climbing to altitude: " + str(self.altitude))
        self.client.moveToPositionAsync(0, 0, z, self.velocity).join()  # 飞到一定高度

        print("flying to first corner of survey box")
        self.client.moveToPositionAsync(x, -self.boxsize, z, self.velocity).join()

        # let it settle there a bit.
        self.client.hoverAsync().join()
        time.sleep(2)

        # after hovering we need to re-enabled api control for next leg of the trip
        self.client.enableApiControl(True)

        # now compute the survey path required to fill the box
        path = []
        distance = 0
        while x < self.boxsize:
            distance += self.boxsize
            path.append(airsim.Vector3r(x, self.boxsize, z))
            x += self.stripewidth
            distance += self.stripewidth
            path.append(airsim.Vector3r(x, self.boxsize, z))
            distance += self.boxsize
            path.append(airsim.Vector3r(x, -self.boxsize, z))
            x += self.stripewidth
            distance += self.stripewidth
            path.append(airsim.Vector3r(x, -self.boxsize, z))
            distance += self.boxsize

        print("starting survey, estimated distance is " + str(distance))
        trip_time = distance / self.velocity
        print("estimated survey time is " + str(trip_time))
        try:
            result = self.client.moveOnPathAsync(path, self.velocity, trip_time, airsim.DrivetrainType.ForwardOnly,
                                                 airsim.YawMode(False, 0), self.velocity + (self.velocity / 2),
                                                 1).join()
        except:
            errorType, value, traceback = sys.exc_info()
            print("moveOnPath threw exception: " + str(value))
            pass

        print("flying back home")
        self.client.moveToPositionAsync(0, 0, z, self.velocity).join()

        if z < -5:
            print("descending")
            self.client.moveToPositionAsync(0, 0, -5, 2).join()

        print("landing...")
        self.client.landAsync().join()

        print("disarming.")
        self.client.armDisarm(False)


if __name__ == "__main__":
    args = sys.argv
    args.pop(0)
    arg_parser = argparse.ArgumentParser("Usage: survey boxsize stripewidth altitude")
    arg_parser.add_argument("--size", type=float, help="size of the box to survey", default=50)   # 搜索正方形的尺寸
    arg_parser.add_argument("--stripewidth", type=float, help="stripe width of survey (in meters)", default=10)  # 条带宽度   行驶道的距离有多远
    arg_parser.add_argument("--altitude", type=float, help="altitude of survey (in positive meters)", default=50) #  高度，
    arg_parser.add_argument("--speed", type=float, help="speed of survey (in meters/second)", default=5)  # 速度
    args = arg_parser.parse_args(args)
    nav = SurveyNavigator(args)
    nav.start()