#! /usr/bin/env python3

import rospy

from geometry_msgs.msg import Twist

rospy.init_node('commander')

# Имя топика должно совпадать с тем, что слушает subscriber!
pub=rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

rospy.loginfo("Waiting for subscribers...")
while pub.get_num_connections() < 1 and not rospy.is_shutdown():
    rospy.sleep(0.1)

rate = rospy.Rate(1) # 1 Гц (отправлять раз в секунду)

while not rospy.is_shutdown():
    msg=Twist()
    msg.linear.x=1

    rospy.loginfo("Sending command: Move Forward")
    pub.publish(msg)
