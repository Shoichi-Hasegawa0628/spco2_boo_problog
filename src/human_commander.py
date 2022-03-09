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
        # n = random.randint(0, len(self.name)-1)
        # TeachingText = self.name[n]
        # TeachingText = "pig_doll"
        # print(TeachingText)
        # step = 1

        TeachingText = input("Please input object word : \n")
        print('Command: ' + 'Bring ' + TeachingText + ' for me\n')
        weight_average_func.execute_weight_average(TeachingText)

        for t in range(0, 8, 2):
            self.pub_end_flag.publish(self.end_flag)
            #time.sleep(1)
        rospy.signal_shutdown("Finised Inference")

        """
        for i in range(len(objects)):
            TeachingText = objects[i]
            print('Command: ' + 'Bring ' + TeachingText + ' for me\n')
            weight_average_func.execute_weight_average(TeachingText)
        """


        """
            FilePath = "/root/HSR/catkin_ws/src/spco2_boo_problog/data/" + str(TeachingText)
            if not os.path.exists(FilePath):
                os.makedirs(FilePath)
            
            # while not rospy.is_shutdown():
            #     self.pub.publish(TeachingText)
    
            while True:
                Next_step = input("Please input start : \n")
    
                bb = rospy.wait_for_message('/yolov5_ros/output/bounding_boxes', BoundingBoxes, timeout=15)
                detect_object_info = bb.bounding_boxes
                img = rospy.wait_for_message('/yolov5_ros/output/image/compressed', CompressedImage, timeout=15)
                detect_img = self.cv_bridge.compressed_imgmsg_to_cv2(img)
                cv2.imwrite(FilePath + "/detect_image_" + str(step) + ".jpg", detect_img)
                object_list = self.extracting_label(detect_object_info)
                print(object_list)
                j = TeachingText in object_list
                if j == True:
                    print("Target Found!!!\n")
                    self.save_data(step, FilePath, object_list)
                    break
    
                print("Don't Found Target")
                self.save_data(step, FilePath, object_list)
                step += 1
    
            return
        """
    def extracting_label(self, detect_object_info):
        object_list = []
        for i in range(len(detect_object_info)):
            object_list.append(detect_object_info[i].Class)
        return object_list

    def save_data(self, step, FilePath, object_list):
        with open(FilePath + "/result_" + str(step) + ".txt", "w") as f:
            f.write("Number of visits:\n")
            f.write("{}\n".format(step))
            f.write("{}".format(object_list))
            f.close()

if __name__ == '__main__':
    rospy.init_node('enter_human_command', anonymous=False)
    enter = EnterCommand()
    enter.StartPublish()
    # rospy.spin()