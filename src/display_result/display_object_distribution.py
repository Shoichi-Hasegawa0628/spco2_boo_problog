#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from flexbe_core import EventState, Logger
from visualization_msgs.msg import Marker, MarkerArray
import time
import csv



class DisplayObjectDistribution():
    def __init__(self):
        self.pub_marker_array = rospy.Publisher("/view_object_existence_points", MarkerArray, queue_size=1)
        self.robot_poses = [[[-0.108671428571429, -0.07486380952381, 0.0], [0.0]], [[-2.62891238095238, -0.370951428571428, 0.0], [0.0]],
                            [[0.834226666666667, -2.2456619047619, 0.0], [0.0]], [[-1.01198761904762, 3.57496285714286, 0.0], [0.0]]]  # sim (修正必要)
        # all_mu = []
        # K = 0
        # for line in open("/root/HSR/catkin_ws/src/spco2_boo_problog/src/display_result/data/place_region/mu.csv",
        #                  'r'):
        #     mu = []  # (x,y,z)
        #     data = line[:].split(',')
        #     mu += [float(data[0])]
        #     mu += [float(data[1])]
        #     mu += [0.0]
        #     all_mu.append(mu)
        #     K += 1
        # for i in range(len(all_mu)):
        #     self.robot_poses[i][0] = all_mu[i]

        self.marker_array_data = MarkerArray()
        self.id_count = 0
        print("Visualization of the object existence points.")


    def object_distribution_draw(self):
        with open("/root/HSR/catkin_ws/src/spco2_boo_problog/src/display_result/data/object_distribute/exp1/case2_cracker-box/SpCo+ProbLog/83/inference_result.csv", 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            self.place_info = list(csv_reader)

        probs = []
        for place in range(len(self.place_info[0])):
            # probs.append(int(float(self.place_info[1][place]) * 100))
            temp = float(self.place_info[1][place]) * 100
            probs.append(round(temp, 1))
        # self.place_info = [["living", "bedroom", "kitchen"], ["0.1", "0.5", "0.4"]]
        print('Inference result: %s' % (self.place_info))

        for place in range(len(self.place_info[0])):
            Logger.loginfo("{}".format(place))
            text_marker, pose_marker = self.init_marker()

            # tmp_prob = int(float(self.place_info[1][place]) * 100)
            tmp_prob = float(self.place_info[1][place]) * 100
            tmp_prob = round(tmp_prob, 1)
            text_marker.text = str(tmp_prob) + "%"
            text_marker.pose.position.x = self.robot_poses[place][0][0] - 0.2
            text_marker.pose.position.y = self.robot_poses[place][0][1] - 0.4
            text_marker.pose.position.z = self.robot_poses[place][0][2]
            text_marker.scale.x = text_marker.scale.x * 1.7
            text_marker.scale.y = text_marker.scale.y * 1.7
            text_marker.scale.z = text_marker.scale.z * 1.7

            if self.place_info[0][place] == "living":
                text_marker.color.r = 0.6
                text_marker.color.g = 0.0
                text_marker.color.b = 0.0

            elif self.place_info[0][place] == "bedroom":
                text_marker.color.r = 0.0
                text_marker.color.g = 0.0
                text_marker.color.b = 0.6
                text_marker.pose.position.x = self.robot_poses[place][0][0] - 0.6

            elif self.place_info[0][place] == "kitchen":
                text_marker.color.r = 0.5
                text_marker.color.g = 0.5
                text_marker.color.b = 0.0

            else:
                text_marker.pose.position.x = self.robot_poses[place][0][0] + 2.2
                text_marker.pose.position.y = self.robot_poses[place][0][1] - 1.5
                text_marker.pose.position.z = self.robot_poses[place][0][2]
                text_marker.color.r = 0.0
                text_marker.color.g = 0.6
                text_marker.color.b = 0.6


            if tmp_prob == max(probs):
                pose_marker.scale.z = pose_marker.scale.z * 2.5
                # pose_marker.scale.x = pose_marker.scale.x * 2
                # pose_marker.scale.y = pose_marker.scale.y * 2
                # pose_marker.scale.z = pose_marker.scale.z * 2
                # text_marker.scale.x = text_marker.scale.x * 1.7
                # text_marker.scale.y = text_marker.scale.y * 1.7
                # text_marker.scale.z = text_marker.scale.z * 1.7

            elif tmp_prob == min(probs):
                pose_marker.scale.z = pose_marker.scale.z * (1 / 3)
                # pose_marker.scale.x = pose_marker.scale.x * 0.8
                # pose_marker.scale.y = pose_marker.scale.y * 0.8
                # pose_marker.scale.z = pose_marker.scale.z * 0.8

            else:
                # pose_marker.scale.x = pose_marker.scale.x * 1.4
                # pose_marker.scale.y = pose_marker.scale.y * 1.4
                pose_marker.scale.z = pose_marker.scale.z * 1
                # text_marker.scale.x = text_marker.scale.x * 1.2
                # text_marker.scale.y = text_marker.scale.y * 1.2
                # text_marker.scale.z = text_marker.scale.z * 1.2

            pose_marker.pose.position.x = self.robot_poses[place][0][0] + 0.7
            pose_marker.pose.position.y = self.robot_poses[place][0][1]
            pose_marker.pose.position.z = self.robot_poses[place][0][2] + (pose_marker.scale.z / 2)

            if self.place_info[0][place] == "living":
                pose_marker.color.r = 0.8
                pose_marker.color.g = 0.0
                pose_marker.color.b = 0.0

            elif self.place_info[0][place] == "bedroom":
                pose_marker.color.r = 0.0
                pose_marker.color.g = 0.0
                pose_marker.color.b = 0.8
                pose_marker.pose.position.x = self.robot_poses[place][0][0] + 0.3

            elif self.place_info[0][place] == "kitchen":
                pose_marker.color.r = 0.8
                pose_marker.color.g = 0.8
                pose_marker.color.b = 0.0

            else:
                pose_marker.color.r = 0.0
                pose_marker.color.g = 0.8
                pose_marker.color.b = 0.8


            self.id_count += 1
            text_marker.id = self.id_count
            text_marker.ns = "marker" + str(self.id_count)
            self.marker_array_data.markers.append(text_marker)
            self.id_count += 1
            pose_marker.id = self.id_count
            pose_marker.ns = "marker" + str(self.id_count)
            self.marker_array_data.markers.append(pose_marker)

        # rospy.sleep(2)
        # self.pub_marker_array.publish(self.marker_array_data)
        # rospy.sleep(2)
        # self.pub_marker_array.publish(self.marker_array_data)

        while not rospy.is_shutdown():
            self.pub_marker_array.publish(self.marker_array_data)


        # ## 確率値が高い場所の名称を渡す。userdataで
        # place_name = self.place_info[0][probs.index(max(probs))]
        # target_position = self.robot_poses[self.place_info[0].index(place_name)]
        # userdata.target_pose = target_position

    def init_marker(self):
        def_text_marker = Marker()
        def_text_marker.type = Marker.TEXT_VIEW_FACING
        def_text_marker.header.frame_id = "map"
        def_text_marker.header.stamp = rospy.get_rostime()
        def_text_marker.action = Marker.ADD
        def_text_marker.scale.x = 0.7
        def_text_marker.scale.y = 0.7
        def_text_marker.scale.z = 0.7
        def_text_marker.lifetime = rospy.Duration(100)
        def_text_marker.color.a = 1

        def_pose_marker = Marker()
        # def_pose_marker.type = Marker.SPHERE
        def_pose_marker.type = Marker.CYLINDER
        def_pose_marker.header.frame_id = "map"
        def_pose_marker.header.stamp = rospy.get_rostime()
        def_pose_marker.action = Marker.ADD
        def_pose_marker.scale.x = 0.7   # 0.3
        def_pose_marker.scale.y = 0.7   # 0.3
        def_pose_marker.scale.z = 0.6
        def_pose_marker.lifetime = rospy.Duration(100)
        def_pose_marker.color.a = 1

        def_pose_marker.pose.orientation.x = 0.0
        def_pose_marker.pose.orientation.y = 0.0
        def_pose_marker.pose.orientation.z = 0.0
        def_pose_marker.pose.orientation.w = 0.0

        return def_text_marker, def_pose_marker



if __name__ == '__main__':
    rospy.init_node('display_object_distribution', anonymous=False)
    display_obj = DisplayObjectDistribution()
    display_obj.object_distribution_draw()
    rospy.spin()