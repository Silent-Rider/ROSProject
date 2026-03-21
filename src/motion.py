#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from move import FollowController

class FollowerNode:
    def __init__(self):
        rospy.init_node(f"follower_node", anonymous=True)

        self.leader_name = rospy.get_param("~leader", "turtle1")
        self.follower_name = rospy.get_param("~follower", "turtle2")

        self.leader_pose = None
        self.follower_pose = None

        self.move = FollowController()

        rospy.Subscriber(f"/{self.leader_name}/pose", Pose, self.leader_cb)
        rospy.Subscriber(f"/{self.follower_name}/pose", Pose, self.follower_cb)
        self.cmd_pub = rospy.Publisher(f"/{self.follower_name}/cmd_vel", Twist, queue_size=10)

        self.timer = rospy.Timer(rospy.Duration(0.1), self.update)

    def leader_cb(self, msg):
        self.leader_pose = msg

    def follower_cb(self, msg):
        self.follower_pose = msg

    def update(self, event):
        if self.leader_pose is None or self.follower_pose is None:
            return

        v, w = self.move.compute_cmd(self.leader_pose, self.follower_pose)

        cmd = Twist()
        cmd.linear.x = v
        cmd.angular.z = w
        self.cmd_pub.publish(cmd)

if __name__ == "__main__":
    FollowerNode()
    rospy.spin()
