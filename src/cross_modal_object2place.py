#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SpCoSLAM-MLDAとMLDAの学習済みパラメータを用いて、
# 物体の単語から場所の単語をクロスモーダル推論するコード

# Standard Library
import csv
import os

# Third Party
import numpy as np
import roslib.packages
import rospy
from std_msgs.msg import String


class CrossModalObject2Place():
    def __init__(self):
        pass

    def word_callback(self, object_name):
        # word = rospy.wait_for_message("/human_command", String, timeout=None)
        # target_name = word.data
        target_name = object_name
        # print(target_name)
        # target_name = "cup"
        prob = self.cross_modal_inference(target_name)
        return prob

    def read_data(self):
        ## データの読み込み
        # π^s
        with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/pi.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                pass
        pi_s_data = row
        del pi_s_data[-1]
        pi = np.array(pi_s_data, dtype=np.float64)
        # print("pi_s :{}\n".format(pi))

        # ξ
        xi = []
        with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/Xi.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                del row[-1]
                xi.append(np.array(row, dtype=np.float64))
        xi = np.array(xi)
        # print("xi: {}\n".format(xi))

        # θ^sw
        theta_sw = []
        with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/W.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                del row[-1]
                theta_sw.append(np.array(row, dtype=np.float64))
        # print("theta_sw: {}\n".format(theta_sw))

        # 場所の単語辞書
        with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/W_list.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                pass
            place_name_list = row
            #del place_name_list[-1]
        #print(place_name_list)

        # 物体の単語辞書
        with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/Object_W_list.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                pass
            object_name_list = row
            # del object_name_list[-1]
        # print(object_name_list)
        return pi, xi, theta_sw, object_name_list, place_name_list

    def save_data(self, prob, place_name, object_name, place_name_list):
        # 推論結果をtxtでまとめて保存
        FilePath = "/root/HSR/catkin_ws/src/spco2_boo_problog/data/" + str(object_name)
        if not os.path.exists(FilePath):
            os.makedirs(FilePath)
        with open(FilePath + "/cross_modal_inference_result.txt", "w") as f:
            f.write("Result of inference:\n")
            f.write("{} = {}\n".format(place_name_list, prob))
            f.write("Most likely place name is {}\n".format(place_name))
            f.close()

        # probLogに活用するためにprobだけcsvで保存
        with open(FilePath + "/prob.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(prob)

    def cross_modal_inference(self, target_name):
        pi, xi, theta_sw, object_name_list, place_name_list = self.read_data()

        """
        w_tのクロスモーダル推論
        P(w_t | o_t) = ∫ P(w_t | C_t) P(C_t | o_t) dC_t
        1. P(C_t | o_t) = P(C_t | π, o_t, ξ) = P(C_t | π) P(o_t | ξ, C_t)
        2. P(w_t | C_t, W)
        3. 周辺化した上で結果を出力させる
        命令された物体の名前と物体の辞書を対応させて、object_name_vectorを生成
        """

        target = object_name_list.index(target_name)
        object_name_vector = np.zeros(len(object_name_list))
        np.put(object_name_vector, [target], 1)

        prob_w_s_t = [0.0 for i in range(len(theta_sw[0]))]  # 場所の単語リスト作成
        for w in range(len(theta_sw[0])):
            for c in range(pi.size):
                prob = object_name_vector.dot(xi[c].T) * pi[c] * theta_sw[c][w]
                # P(o_t | xi_c^s) P(C^s | pi) P (w^s | theta^sw_c^s)
                prob_w_s_t[w] += prob

        prob_w_s_t_r = [float(j) / sum(prob_w_s_t) for j in prob_w_s_t]  # 正規化
        # print("Result of inference:")
        # print("{} = {}\n".format(place_name_list, prob_w_s_t_r))

        """
        # 降順で表示するために辞書を作る
        dic = {}
        for i in range(len(place_name_list)):
            dic[place_name_list[i]] = str(prob_w_s_t[i])
        print(dic)
        """

        # w_s_t = np.argmax(prob_w_s_t_r)
        #print("Most likely place is {}\n".format(place_name_list[w_s_t], w_s_t))

        # prob_sort = sorted(prob_w_s_t_r, reverse=True)
        """
        max_place_name_list = []
        for i in range(len(prob_sort)):
            max_place_name_list.append()
        print(max_place_name_list)
        """
        #print("Arranged in descending order of probability:")
        #print("{}\n".format(prob_sort))
        # print(prob_w_s_t_r)
        # print(place_name_list)
        # print(target_name)
        # print(place_name_list)

        # self.save_data(prob_w_s_t_r, place_name_list[w_s_t], target_name, place_name_list)
        #print(prob_w_s_t_r)
        return prob_w_s_t_r


if __name__ == "__main__":
    # rospy.init_node('cross_modal_object2place')
    cross_modal = CrossModalObject2Place()
    # cross_modal.word_callback()
    # rospy.spin()
