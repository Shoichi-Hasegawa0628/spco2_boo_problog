#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ProbLogの確率とSpCoSLAM-MLDAの確率を重み平均してどの場所が一番高確率かを出力するコード

# Standard Library
import sys
sys.path.append('/root/HSR/catkin_ws/src/problog_ros/src')
#print (sys.path)
import random
import csv
import os

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
        # self.place_id_pub = rospy.Publisher("/place_id", String, queue_size=10)
        # self.spco_params_path = str(roslib.packages.get_pkg_dir("rgiro_spco2_slam")) + "/data/output/test/max_likelihood_param/"


    def execute_weight_average(self, object_name):
        # word = rospy.wait_for_message("/human_command", String, timeout=None)
        # for i in range(len(objects)):
        target_name = object_name #word.data #objects[i]
        # Problogの呼び出し
        #print("ProbLog Start")
        problog_probs_rd = []
        problog_probs = self.logical.word_callback(target_name)
        for i in range(len(problog_probs)):
            problog_probs_rd.append(round(problog_probs[i], 2))
        #problog_probs_rd = round(problog_probs, 2)
        #print("< ProbLog Result >")
        #print("[living, bedroom, kitchen, bathroom] = {}".format(problog_probs_rd))
        #print("****************************************************************\n")


        # Cross-modal Inferenceの呼び出し
        #print("SpCoSLAM-MLDA Start")
        # rospy.wait_for_message("/human_command", String, timeout=None)
        cross_modal_probs_rd = []
        cross_modal_probs = self.cross_modal.word_callback(target_name)
        for i in range(len(cross_modal_probs)):
            cross_modal_probs_rd.append(round(cross_modal_probs[i], 2))
        #cross_modal_probs_rd = round(cross_modal_probs, 2)
        # cross_modal_probs = [0.25, 0.25, 0.25, 0.25]
        #print("< Cross-modal-inference (SpCoSLAM) Result >")
        #print("[living, bedroom, kitchen, bathroom] = {}".format(cross_modal_probs_rd))
        #print("****************************************************************\n")


        # 重み平均
        #weight_average_probs = (problog_probs + cross_modal_probs) * eta
        weight_average_probs = (eta * np.asarray(problog_probs)) + ((1 - eta) * np.asarray(cross_modal_probs))
        weight_average_probs_rd = []
        for i in range(len(weight_average_probs)):
            weight_average_probs_rd.append(round(weight_average_probs[i], 2))
        #weight_average_probs_rd = [round(weight_average_probs[i], 2) for i in weight_average_probs]
        #weight_average_probs_rd = round(weight_average_probs, 2)
        #print(sum(weight_average_probs))
        print("< Weight average processing Result (weight is 0.17) >")
        print("[living, bedroom, kitchen, bathroom] = {}".format(weight_average_probs_rd))
        print("****************************************************************\n")


        # 場所の単語一覧をロード
        place_name_list = []
        for line in open('W_list.csv', 'r'):
            itemList = line[:-1].split(',')
            #if(i == 1):
            for j in range(len(itemList)):
                if (itemList[j] != ""):
                    place_name_list = place_name_list + [itemList[j]]

        # 最大確率が同一の場合は、いずれかをランダムに選択 (重み)
        max_prob = max(weight_average_probs_rd)
        max_probs_idxs = np.where(weight_average_probs_rd == max_prob)
        max_probs_idx = max_probs_idxs[0]

        if len(max_probs_idx) > 1:
            print("Multiple max probability !")
            target_place_id = max_probs_idx[random.randrange(len(max_probs_idx))]
        else:
            target_place_id = max_probs_idx[0]

        print("Target Place Name: {}\n".format(place_name_list[target_place_id]))
        print("Max Probability: {}\n".format(max_prob))
        # return target_place_id

        weight_sort = sorted(weight_average_probs_rd, reverse=True)
        print("Arranged in descending order of probability:")
        print("{} = {}\n".format(["1st: living", "2nd: bedroom", "3rd: kitchen", "4th: bathroom"], weight_sort))
        self.save_data(weight_average_probs_rd, place_name_list, target_name)

    def save_data(self, prob, place_name_list, object_name):
        # 推論結果をtxtでまとめて保存
        FilePath = "/root/HSR/catkin_ws/src/spco2_boo_problog/data/" + str(object_name)
        if not os.path.exists(FilePath):
            os.makedirs(FilePath)
        with open(FilePath + "/inference_result.txt", "w") as f:
            f.write("Result of inference:\n")
            f.write("{} = {}\n".format(place_name_list, prob))
            f.close()



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

    # r = rospy.Rate(10)
    # while not rospy.is_shutdown():
    #     weight_average.place_id_pub.publish(str(place_id))
    # r.sleep()
    # #rospy.spin()
