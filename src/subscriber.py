#! /usr/bin/env python3

import rospy

from geometry_msgs.msg import Twist

def callback(msg):
    rospy.loginfo(f"Received: Linear X={msg.linear.x}")

rospy.init_node('command_listener')

# Имя топика должно совпадать с тем, куда пишет publisher!
rospy.Subscriber('/command', Twist, callback)
rospy.spin()