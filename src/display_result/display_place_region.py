#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Pose
import tf

import math
import numpy as np
import sys
sys.path.append("lib/")
# from __init__ import *


class DisplayPlaceRegion():
    def __init__(self):
        self.pub_spatial_distribution = rospy.Publisher('/draw_space', MarkerArray, queue_size=10)


    def spatial_distribution_draw(self):
        Number = None
        RAD_90 = math.radians(90)
        color_all = 1  # 1 or 0 、(0ならばすべて赤)
        mu_draw = 1  # 1 or 0 、(0ならば中心値を表示しない)
        sigma_draw = 1  # 1 or 0, (0ならば分散を表示しない)
        mu_arrow = 0  # 矢印を可視化する場合
        COLOR = [
            [1, 0, 0], [0, 0, 1], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], # 4
            [0, 1, 0], [0.8, 0.1, 0.1], [0.1, 0.8, 0.1], [0.1, 0.1, 0.8], [0.6, 0.2, 0.2],  # 9
            [0.2, 0.6, 0.2], [0.2, 0.2, 0.6], [0.4, 0.3, 0.3], [0.3, 0.4, 0.3], [0.3, 0.3, 0.4],  # 14
            [0.7, 0.2, 0.1], [0.7, 0.1, 0.2], [0.2, 0.7, 0.1], [0.1, 0.7, 0.2], [0.2, 0.1, 0.7],  # 19
            [0.1, 0.2, 0.7], [0.5, 0.2, 0.3], [0.5, 0.3, 0.2], [0.3, 0.5, 0.2], [0.2, 0.5, 0.3],  # 24
            [0.3, 0.2, 0.5], [0.2, 0.3, 0.5], [0.7, 0.15, 0.15], [0.15, 0.7, 0.15], [0.15, 0.15, 0.7],  # 29
            [0.6, 0.3, 0.1], [0.6, 0.1, 0.3], [0.1, 0.6, 0.3], [0.3, 0.6, 0.1], [0.3, 0.1, 0.6],  # 34
            [0.1, 0.3, 0.6], [0.8, 0.2, 0], [0.8, 0, 0.2], [0.2, 0.8, 0], [0, 0.8, 0.2],  # 39
            [0.2, 0, 0.8], [0, 0.2, 0.8], [0.7, 0.3, 0], [0.7, 0, 0.3], [0.3, 0.7, 0.0],  # 44
            [0.3, 0, 0.7], [0, 0.7, 0.3], [0, 0.3, 0.7], [0.25, 0.25, 0.5], [0.25, 0.5, 0.25],  # 49
            [1, 0, 0], [0, 1, 0], [0, 0, 1], [0.5, 0.5, 0], [0.5, 0, 0.5],  # 54
            [0, 0.5, 0.5], [0.8, 0.1, 0.1], [0.1, 0.8, 0.1], [0.1, 0.1, 0.8], [0.6, 0.2, 0.2],  # 59
            [0.2, 0.6, 0.2], [0.2, 0.2, 0.6], [0.4, 0.3, 0.3], [0.3, 0.4, 0.3], [0.3, 0.3, 0.4],  # 64
            [0, 7, 0.2, 0.1], [0.7, 0.1, 0.2], [0.2, 0.7, 0.1], [0.1, 0.7, 0.2], [0.2, 0.1, 0.7],  # 69
            [0.1, 0.2, 0.7], [0.5, 0.2, 0.3], [0.5, 0.3, 0.2], [0.3, 0.5, 0.2], [0.2, 0.5, 0.3],  # 74
            [0.3, 0.2, 0.5], [0.2, 0.3, 0.5], [0.7, 0.15, 0.15], [0.15, 0.7, 0.15], [0.15, 0.15, 0.7],  # 79
            [0.6, 0.3, 0.1], [0.6, 0.1, 0.3], [0.1, 0.6, 0.3], [0.3, 0.6, 0.1], [0.3, 0.1, 0.6],  # 84
            [0.1, 0.3, 0.6], [0.8, 0.2, 0], [0.8, 0, 0.2], [0.2, 0.8, 0], [0, 0.8, 0.2],  # 89
            [0.2, 0, 0.8], [0, 0.2, 0.8], [0.7, 0.3, 0], [0.7, 0, 0.3], [0.3, 0.7, 0.0],  # 94
            [0.3, 0, 0.7], [0, 0.7, 0.3], [0, 0.3, 0.7], [0.25, 0.25, 0.5], [0.25, 0.5, 0.25]  # 99
        ]

        # 最大尤度のパーティクルのmuとsigを読み込み
        mu_all, Class_NUM = self.mu_read()
        sigma = self.sigma_read()
        data_class = [i for i in range(Class_NUM)]
        marker_array = MarkerArray()
        id = 0
        for c in data_class:
            # 場所領域の中心値を示す場合
            # ===場所領域の範囲の可視化====================
            if sigma_draw == 1:

                marker = Marker()
                marker.type = Marker.CYLINDER

                (eigValues, eigVectors) = np.linalg.eig(sigma[c])
                angle = (math.atan2(eigVectors[1, 0], eigVectors[0, 0]))

                marker.scale.x = 2 * math.sqrt(eigValues[0])
                marker.scale.y = 2 * math.sqrt(eigValues[1])

                marker.pose.orientation.w = math.cos(angle * 0.5)
                marker.pose.orientation.z = math.sin(angle * 0.5)

                marker.scale.z = 0.01  # default: 0.05
                marker.color.a = 0.5
                marker.header.frame_id = 'map'
                marker.header.stamp = rospy.get_rostime()
                marker.id = id
                id += 1
                marker.action = Marker.ADD
                marker.pose.position.x = mu_all[c][0]
                marker.pose.position.y = mu_all[c][1]
                marker.color.r = COLOR[c][0]  # default: COLOR[c][0] 色のばらつきを広げる
                marker.color.g = COLOR[c][1]  # default: COLOR[c][1] 色のばらつきを広げる
                marker.color.b = COLOR[c][2]  # default: COLOR[c][2] 色のばらつきを広げる

                if Number != None:
                    if Number == c:
                        marker_array.markers.append(marker)
                else:
                    marker_array.markers.append(marker)
            if mu_draw == 1:
                mu_marker = Marker()

                if mu_arrow == 1:  # 矢印を可視化する場合
                    mu_marker.type = Marker.ARROW
                    orient_cos = mu_all[c][3]
                    orient_sin = mu_all[c][2]
                    if orient_sin > 1.0:
                        orient_sin = 1.0
                    elif orient_sin < -1.0:
                        orient_sin = -1.0
                    # radian xを導出
                    radian = math.asin(orient_sin)
                    if orient_sin > 0 and orient_cos < 0:
                        radian = radian + RAD_90
                    elif orient_sin < 0 and orient_cos < 0:
                        radian = radian - RAD_90

                    mu_marker.pose.orientation.z = math.sin(radian / 2.0)
                    mu_marker.pose.orientation.w = math.cos(radian / 2.0)
                    # <<<<<<<矢印の大きさ変更>>>>>>>>>>>>>>>>>>>>>>>>
                    mu_marker.scale.x = 0.5  # default: 0.4
                    mu_marker.scale.y = 0.07  # default: 0.1
                    mu_marker.scale.z = 0.001  # default: 1.0
                    mu_marker.color.a = 1

                elif mu_arrow == 0:
                    mu_marker.type = Marker.SPHERE
                    mu_marker.scale.x = 0.1
                    mu_marker.scale.y = 0.1
                    mu_marker.scale.z = 0.01  # default: 0.05
                    mu_marker.color.a = 1.0

                mu_marker.header.frame_id = 'map'
                mu_marker.header.stamp = rospy.get_rostime()
                mu_marker.id = id
                id += 1
                mu_marker.action = Marker.ADD
                mu_marker.pose.position.x = mu_all[c][0]
                mu_marker.pose.position.y = mu_all[c][1]
                # print c,mu_marker.pose.position.x,mu_marker.pose.position.y

                if color_all == 1:
                    mu_marker.color.r = COLOR[c][0]  # default: COLOR[c][0]
                    mu_marker.color.g = COLOR[c][1]  # default: COLOR[c][1]
                    mu_marker.color.b = COLOR[c][2]  # default: COLOR[c][2]
                elif color_all == 0:
                    mu_marker.color.r = 1.0
                    mu_marker.color.g = 0
                    mu_marker.color.b = 0

                if Number != None:
                    if Number == c:
                        marker_array.markers.append(mu_marker)
                else:
                    marker_array.markers.append(mu_marker)

        # rospy.sleep(2)
        # self.pub_spatial_distribution.publish(marker_array)
        # rospy.sleep(2)
        # self.pub_spatial_distribution.publish(marker_array)

        while not rospy.is_shutdown():
            self.pub_spatial_distribution.publish(marker_array)


    def sigma_read(self):
        all_sigma = []
        for line in open("/root/HSR/catkin_ws/src/spco2_boo_problog/src/display_result/data/place_region/exp2/88/sig.csv",
                         'r'):
            data = line[:].split(',')
            sigma = [[float(data[0]), float(data[1]), 0, 0], [float(data[2]), float(data[3]), 0, 0], [0, 0, 0, 0],
                     [0, 0, 0, 0]]
            all_sigma.append(sigma)
        return all_sigma

    def mu_read(self):
        all_mu = []
        K = 0
        for line in open("/root/HSR/catkin_ws/src/spco2_boo_problog/src/display_result/data/place_region/exp2/88/mu.csv",
                         'r'):
            mu = []  # (x,y,sin,cos)
            data = line[:].split(',')
            mu += [float(data[0])]
            mu += [float(data[1])]
            mu += [0]  # float(data[2])]
            mu += [0]  # float(data[3])]
            all_mu.append(mu)
            K += 1
        return all_mu, K


if __name__ == '__main__':
    rospy.init_node('display_place_region', anonymous=False)
    display_place = DisplayPlaceRegion()
    display_place.spatial_distribution_draw()
    rospy.spin()
