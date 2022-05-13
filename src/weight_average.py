#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ProbLogの確率とSpCoSLAM-MLDAの確率を重み平均してどの場所が一番高確率かを出力するコード

# Standard Library
import sys

sys.path.append('/root/HSR/catkin_ws/src/problog_ros/src')
# print (sys.path)
import random
import csv
import os
import itertools

# Third Party
import rospy
import output_logical_inference
import output_prior_knowledge
import cross_modal_object2place
import numpy as np
from std_msgs.msg import String
import roslib.packages

# Self-made Modules
from __init__ import *


class WeightAverageProbability():
    def __init__(self):
        self.prior_knowledge = output_prior_knowledge.OutputPriorKnowledge()
        self.logical = output_logical_inference.LogicalInference()
        self.cross_modal = cross_modal_object2place.CrossModalObject2Place()
        # self.place_id_pub = rospy.Publisher("/place_id", String, queue_size=10)
        # self.spco_params_path = str(roslib.packages.get_pkg_dir("rgiro_spco2_slam")) + "/data/output/test/max_likelihood_param/"

    def execute_weight_average(self, object_name):
        # word = rospy.wait_for_message("/human_command", String, timeout=None)
        # for i in range(len(objects)):
        target_name = object_name  # word.data #objects[i]

        #　場所の単語情報の読み込み
        with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/W_list.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                pass
            place_name_list_s = row
        place_name_list_s.pop(-1)

        problog_probs_r = [0 for i in range(len(place_name_list_s))]  # 場所概念の単語数に合わせた表現 (論理推論)
        prior_probs_r = [0 for i in range(len(place_name_list_s))]  # 場所概念の単語数に合わせた表現 (Prior)

        place_name_list_l = ["living", "kitchen", "bedroom", "bathroom", "entrance", "study_room"]


        # 事前知識の呼び出し
        prior_probs_rd = []
        prior_probs = self.prior_knowledge.word_callback(target_name)
        # print(prior_probs)

        # 場所の単語の呼び出し for文ではじめる
        # 場所の単語のindexを調べる
        # print(place_name_list_s[0])
        # print(place_name_list_l[0])
        # print(place_name_list_s[0] in place_name_list_l)

        for j in range(len(place_name_list_s)):
            if ((place_name_list_s[j] in place_name_list_l) == True):
                a = place_name_list_l.index(place_name_list_s[j])
                prior_probs_r[j] = prior_probs[a]
            else:
                prior_probs_r[j] = 0
        #
        # for i in range(len(prior_probs)):
        #     prior_probs_rd.append(round(prior_probs[i], 2))
        #problog_probs_rd = round(problog_probs, 2)
        print("< Prior Result >")
        print("{} = {}".format(place_name_list_s, prior_probs_r))
        print("****************************************************************\n")
        # print(sum(prior_probs_r))

        # Problogの呼び出し
        print("ProbLog Start")
        problog_probs_rd = []
        problog_probs = self.logical.word_callback(target_name)
        # print(problog_probs)

        # 場所の単語の呼び出し for文ではじめる
        # 場所の単語のindexを調べる
        for j in range(len(place_name_list_s)):
            if ((place_name_list_s[j] in place_name_list_l) == True):
                a = place_name_list_l.index(place_name_list_s[j])
                problog_probs_r[j] = problog_probs[a]
            else:
                problog_probs_r[j] = 0

        # for i in range(len(problog_probs)):
        #     problog_probs_rd.append(round(problog_probs[i], 2))
        # problog_probs_rd = round(problog_probs, 2)
        print("< ProbLog Result >")
        print("{} = {}".format(place_name_list_s, problog_probs_r))
        print("****************************************************************\n")
        # print(sum(problog_probs_r))

        # Cross-modal Inferenceの呼び出し
        print("SpCoSLAM Start")
        # rospy.wait_for_message("/human_command", String, timeout=None)
        cross_modal_probs_rd = []
        cross_modal_probs = self.cross_modal.word_callback(target_name)
        print(cross_modal_probs)
        for i in range(len(cross_modal_probs)):
            cross_modal_probs_rd.append(round(cross_modal_probs[i], 2))
        # cross_modal_probs_rd = round(cross_modal_probs, 2)
        # cross_modal_probs = [0.25, 0.25, 0.25, 0.25]
        print("< Cross-modal-inference (SpCoSLAM) Result >")
        print("{} = {}".format(place_name_list_s, cross_modal_probs_rd))
        print("****************************************************************\n")
        # print(sum(cross_modal_probs))

        # 重み平均
        # weight_average_probs = cross_modal_probs # SpCo
        # weight_average_probs = (eta * np.asarray(prior_probs)) + ((1 - eta) * np.asarray(cross_modal_probs)) # SpCo + Prior
        weight_average_probs = (eta * np.asarray(problog_probs_r)) + (
                    (1 - eta) * np.asarray(cross_modal_probs))  # SpCo + ProbLog
        weight_average_probs_rd = []
        for i in range(len(weight_average_probs)):
            weight_average_probs_rd.append(round(weight_average_probs[i], 2))
        # weight_average_probs_rd = [round(weight_average_probs[i], 2) for i in weight_average_probs]
        # weight_average_probs_rd = round(weight_average_probs, 2)
        # print(sum(weight_average_probs))
        print("< Weight average processing Result >")
        print("{} = {}".format(place_name_list_s, weight_average_probs))
        print("****************************************************************\n")
        # print(sum(weight_average_probs))

        # # 場所の単語一覧をロード
        # place_name_list = []
        # for line in open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/W_list.csv', 'r'):
        #     itemList = line[:-1].split(',')
        #     # if(i == 1):
        #     for j in range(len(itemList)):
        #         if (itemList[j] != ""):
        #             place_name_list = place_name_list + [itemList[j]]
        #
        # # 最大確率が同一の場合は、いずれかをランダムに選択 (重み)
        # max_prob = max(weight_average_probs_rd)
        # max_probs_idxs = np.where(weight_average_probs_rd == max_prob)
        # max_probs_idx = max_probs_idxs[0]
        #
        # if len(max_probs_idx) > 1:
        #     print("Multiple max probability !")
        #     target_place_id = max_probs_idx[random.randrange(len(max_probs_idx))]
        # else:
        #     target_place_id = max_probs_idx[0]

        # print("Target Place Name: {}\n".format(place_name_list[target_place_id]))
        # print("Max Probability: {}\n".format(max_prob))
        # return target_place_id

        """
        weight_sort = sorted(weight_average_probs_rd, reverse=True)
        print("Arranged in descending order of probability:")
        print("{} = {}\n".format(["1st: living", "2nd: bedroom", "3rd: kitchen", "4th: bathroom"], weight_sort))
        """
        # self.save_data(weight_average_probs_rd, place_name_list, target_name)
        return weight_average_probs


    def save_data(self, prob, place_name_list, object_name):
        FilePath = "/root/HSR/catkin_ws/src/spco2_boo_problog/data/" + str(object_name)
        if not os.path.exists(FilePath):
            os.makedirs(FilePath)

        save_data = []
        save_data.append(place_name_list)
        save_data.append(prob)

        with open(FilePath + "/inference_result.csv", "w") as f:
            write = csv.writer(f)
            write.writerows(save_data)


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
        return


if __name__ == "__main__":
    # rospy.init_node('weight_avarage')
    weight_average = WeightAverageProbability()
    probs = weight_average.execute_weight_average("pig_doll")

    # r = rospy.Rate(10)
    # while not rospy.is_shutdown():
    #     weight_average.place_id_pub.publish(str(place_id))
    # r.sleep()
    # #rospy.spin()
