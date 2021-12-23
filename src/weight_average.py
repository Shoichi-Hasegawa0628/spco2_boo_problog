#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ProbLogの確率とSpCoSLAM-MLDAの確率を重み平均してどの場所が一番高確率かを出力するコード

# Standard Library
import sys
sys.path.append('/root/RULO/catkin_ws/src/problog_ros/src')
#print (sys.path)
import random
import csv

# Third Party
import rospy
import problog_ros_output_prob
import cross_modal_object2place
import numpy as np
from std_msgs.msg import String
import roslib.packages

# Self-made Modules
from __init__ import *


class WeightAverageProbability():
    def __init__(self):
        self.logical = problog_ros_output_prob.LogicalInference()
        self.cross_modal = cross_modal_object2place.CrossModalObject2Place()
        self.place_id_pub = rospy.Publisher("/place_id", String, queue_size=10)
        self.spco_params_path = str(roslib.packages.get_pkg_dir("rgiro_spco2_slam")) + "/data/output/test/max_likelihood_param/"
        pass


    def execute_weight_average(self):
        
        # Problogの呼び出し
        #print("ProbLog Start")
        problog_probs = self.logical.word_callback()
        print("< ProbLog Result >\n")
        print("[living, kitchen, bedroom, toilet] = {}\n".format(problog_probs))
        print("****************************************************************\n")
        
 
        # Cross-modal Inferenceの呼び出し
        #print("SpCoSLAM-MLDA Start")
        rospy.wait_for_message("/human_command", String, timeout=None)
        cross_modal_probs = self.cross_modal.word_callback()
        print("< Ancestral Sampling (SpCoSLAM-MLDA) Result >\n")
        print("[living, kitchen, bedroom, toilet] = {}\n".format(cross_modal_probs))
        print("****************************************************************\n")

        
        # 重み平均
        #weight_average_probs = (problog_probs + cross_modal_probs) * eta
        weight_average_probs = (eta * np.asarray(problog_probs)) + ((1 - eta) * np.asarray(cross_modal_probs))
        #print(sum(weight_average_probs))
        print("< Weight average processing Result >\n")
        print("[living, kitchen, bedroom, toilet] = {}\n".format(weight_average_probs))
        print("****************************************************************\n")
        

        # 場所の単語一覧をロード
        place_name_list = []
        for line in open(self.spco_params_path + 'W_list.csv', 'r'):
            itemList = line[:-1].split(',')
            #if(i == 1):
            for j in xrange(len(itemList)):
                if (itemList[j] != ""):
                    place_name_list = place_name_list + [itemList[j]]

        # 最大確率が同一の場合は、いずれかをランダムに選択 (重み)
        max_prob = max(weight_average_probs)
        max_probs_idxs = np.where(weight_average_probs == max_prob)
        max_probs_idx = max_probs_idxs[0]

        if len(max_probs_idx) > 1:
            print("Multiple max probability !")
            target_place_id = max_probs_idx[random.randrange(len(max_probs_idx))]
        else:
            target_place_id = max_probs_idx[0]

        print("Target Place Name and ID for SpCoNavi: {}, {}\n".format(place_name_list[target_place_id], target_place_id))
        print("Max Probability: {}\n".format(max_prob))
        return target_place_id
    

        """
        # 最大確率が同一の場合は、いずれかをランダムに選択 (cross)
        max_prob = max(cross_modal_probs)
        max_probs_idxs = np.where(cross_modal_probs == max_prob)
        max_probs_idx = max_probs_idxs[0]
        

        if len(max_probs_idx) > 1:
            print("Multiple max probability !")
            target_place_id = max_probs_idx[random.randrange(len(max_probs_idx))]
        else:
            target_place_id = max_probs_idx[0]

        print("Target Place Name and ID for SpCoNavi: {}, {}\n".format(place_name_list[target_place_id], target_place_id))
        print("Max Probability: {}\n".format(max_prob))
        return target_place_id
        """
        

if __name__ == "__main__":
    rospy.init_node('weight_avarage')
    weight_average = WeightAverageProbability()
    place_id = weight_average.execute_weight_average()

    r = rospy.Rate(10) 
    while not rospy.is_shutdown():
        weight_average.place_id_pub.publish(str(place_id))
    r.sleep()
    #rospy.spin()
