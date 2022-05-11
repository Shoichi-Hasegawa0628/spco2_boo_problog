#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from visualization_msgs.msg import Marker


class DisplayObjectExistenceResultRviz():
    def __init__(self):
        self.pub_object_txt = rospy.Publisher("/object_existence_prob_text", Marker, queue_size=10)
        self.pub_object_shape = rospy.Publisher("/object_existence_prob_shape", Marker, queue_size=10)
        self.rate = rospy.Rate(25)

    def display_result(self):
        while not rospy.is_shutdown():
            marker_data_text = Marker()
            marker_data_text.header.frame_id = "map"
            marker_data_text.header.stamp = rospy.Time.now()

            marker_data_text.ns = "basic_shapes"
            marker_data_text.id = 0

            marker_data_text.action = Marker.ADD

            marker_data_text.pose.position.x = 0.0
            marker_data_text.pose.position.y = 0.0
            marker_data_text.pose.position.z = 0.0

            marker_data_text.pose.orientation.x = 0.0
            marker_data_text.pose.orientation.y = 0.0
            marker_data_text.pose.orientation.z = 1.0
            marker_data_text.pose.orientation.w = 0.0

            marker_data_text.color.r = 1.0
            marker_data_text.color.g = 0.0
            marker_data_text.color.b = 0.0
            marker_data_text.color.a = 1.0

            marker_data_text.scale.x = 1
            marker_data_text.scale.y = 0.1
            marker_data_text.scale.z = 0.1

            marker_data_text.lifetime = rospy.Duration()

            marker_data_text.type = 9
            marker_data_text.text = "blablabla"

            self.pub_object_txt.publish(marker_data_text)
            self.rate.sleep()


if __name__ == "__main__":
    rospy.init_node('display_object_existence_result_rviz')
    display_object_result = DisplayObjectExistenceResultRviz()
    # cross_modal.word_callback()
    rospy.spin()
