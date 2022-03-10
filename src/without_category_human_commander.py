#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Terminal経由で探索すべき物体を送信するコード

import rospy
from std_msgs.msg import String
import random
import randomization_selection
from sensor_msgs.msg import CompressedImage
from yolo_ros_msgs.msg import BoundingBoxes, BoundingBox
import cv2
from cv_bridge import CvBridge, CvBridgeError
import os
import time
import weight_average
import cross_modal_object2place
from std_msgs.msg import Empty, String
import csv
cross_modal_object2place_func = cross_modal_object2place.CrossModalObject2Place()
weight_average_func = weight_average.WeightAverageProbability()
# import randomization_selection
# random_select_func = randomization_selection.RandomizationSelection()
from __init__ import *

class EnterCommand():
    def __init__(self):
        self.cv_bridge = CvBridge()
        # self.pub_place_name = rospy.Publisher("/place_name", String, queue_size=10)
        self.end_flag = Empty()
        self.pub_end_flag = rospy.Publisher("/end_flag", Empty, queue_size=10)

    def StartPublish(self): 


        #TeachingText = input("Please input object word : \n")
        TeachingText = "penguin_doll"
        print('Command: ' + 'Bring ' + TeachingText + ' for me\n')
        # weight_average_func.execute_weight_average(TeachingText)


        FilePath = "/root/HSR/catkin_ws/src/spco2_boo_problog/data/" + str(TeachingText)
        if not os.path.exists(FilePath):
            os.makedirs(FilePath)

        save_data = []
        save_data.append(["living", "bedroom", "kitchen"])
        save_data.append([0.33, 0.33, 0.33])

        with open(FilePath + "/inference_result.csv", "w") as f:
            write = csv.writer(f)
            write.writerows(save_data)

        while not rospy.is_shutdown():
        #for t in range(0, 8, 2):
            self.pub_end_flag.publish(self.end_flag)
            #time.sleep(1)
            rospy.Rate(10).sleep()





        # bb = rospy.wait_for_message('/yolov5_ros/output/bounding_boxes', BoundingBoxes, timeout=15)
        # detect_object_info = bb.bounding_boxes
        #
        # object_list = self.extracting_label(detect_object_info)
        # print(object_list)
        # j = "orange" in object_list
        # if j == True:
        #     print("Target Found!!!\n")




        return



    def extracting_label(self, detect_object_info):
        object_list = []
        for i in range(len(detect_object_info)):
            object_list.append(detect_object_info[i].Class)
        return object_list

    # def save_data(self, step, FilePath, object_list):
    #     with open(FilePath + "/result_" + str(step) + ".txt", "w") as f:
    #         f.write("Number of visits:\n")
    #         f.write("{}\n".format(step))
    #         f.write("{}".format(object_list))
    #         f.close()

if __name__ == '__main__':
    rospy.init_node('enter_human_command', anonymous=False)
    enter = EnterCommand()
    enter.StartPublish()
    # rospy.spin()