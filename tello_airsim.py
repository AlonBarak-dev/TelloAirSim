from Server_ControlDrone import ServerThread


class TelloAirSimApi:


    def __init__(self):
        self.airsim_ctlr = ServerThread()

    def send_rc_control(self, left_right_velocity: int, forward_backward_velocity:int,
                         up_down_velocity: int, yaw_velocity: int) -> None:

        if forward_backward_velocity > 0:
            # forward
            self.airsim_ctlr.forward(forward_backward_velocity)
        else:
            # backward
            self.airsim_ctlr.back(-forward_backward_velocity)

        if left_right_velocity > 0:
            # right
            self.airsim_ctlr.right(left_right_velocity)
        else:
            # left
            self.airsim_ctlr.left(-left_right_velocity)

        if up_down_velocity > 0:
            # up
            self.airsim_ctlr.up(up_down_velocity)
        else:
            # down
            self.airsim_ctlr.down(-up_down_velocity)
        
        if yaw_velocity > 0:
            # yaw right
            self.airsim_ctlr.turnRight(yaw_velocity)
        else:
            # yaw left
            self.airsim_ctlr.turnLeft(-yaw_velocity)
        
    def takeoff(self):
        self.airsim_ctlr.takeoff()