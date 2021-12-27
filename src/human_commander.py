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
import weight_average
import cross_modal_object2place
cross_modal_object2place_func = cross_modal_object2place.CrossModalObject2Place()
weight_average_func = weight_average.WeightAverageProbability()
# import randomization_selection
# random_select_func = randomization_selection.RandomizationSelection()

class EnterCommand():
    def __init__(self):
        self.cv_bridge = CvBridge()
        # self.object_list = []
        # self.pub = rospy.Publisher('/human_command', String, queue_size=1) ## queue size is not important for sending just one messeage.
        # self.name = ["blue_cup", "green_cup", "orange_cup","penguin_doll", "pig_doll", "sheep_doll","coffee_bottle", "fruits_bottle", "muscat_bottle"]


        """
        物体の名前一覧 (Problogに依存)
        
            cup>>>
                blue_cup
				green_cup
				orange_cup

			doll>>>
				penguin_doll
				pig_doll
				sheep_doll
			
            bottle>>>
				coffee_bottle
				fruits_bottle
				muscat_bottle
        """
        pass


    def StartPublish(self): 
        # n = random.randint(0, len(self.name)-1)
        # TeachingText = self.name[n]
        # TeachingText = "pig_doll"
        # print(TeachingText)
        step = 1
        TeachingText = input("Please input object word : \n")

        """
        if (get_key == "spawn"):
            print(get_key)
            spawn_many_model.spawn_model("model")
            break
        elif (get_key == "delete"):
            print(get_key)
            spawn_many_model.all_delete_model()
            break
        print("The command is different, please enter the correct command.\n")
        """
        print('Command: ' + 'Bring ' + TeachingText + ' for me\n')
        weight_average_func.execute_weight_average(TeachingText)
        # cross_modal_object2place_func.word_callback(TeachingText)
        # random_select_func.selection(TeachingText)
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