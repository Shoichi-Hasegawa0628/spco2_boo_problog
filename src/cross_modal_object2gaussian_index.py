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

import weight_average


class CrossModalObject2Place():
    def __init__(self):
        self.weight_ave = weight_average.WeightAverageProbability()
        self.callback()

    # def callback(self, prob_w_o):
    def callback(self):
        # word = rospy.wait_for_message("/human_command", String, timeout=None)
        # target_name = word.data
        # target_name = object_name
        # print(target_name)
        # target_name = "cup"
        prob_w_o = self.weight_ave.execute_weight_average("pig_doll")
        # prob_w_o = [1/221 for i in range(221)] #ダミー
        self.cross_modal_inference(prob_w_o)

        return

    def read_data(self):
        ## データの読み込み
        ## 必要なもの P (i_t | w_t)：W, pi, Φ, W_list
        ## 必要なもの P (w_t | O_t)：論理推論の結果 or Priorの結果 or クロスモーダル推論 (pi, ξ, W, W_list, Object_W_list)

        # π
        with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/pi.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                pass
        pi_s_data = row
        del pi_s_data[-1]
        pi = np.array(pi_s_data, dtype=np.float64)
        # print("pi_s :{}\n".format(pi))

        # ξ
        # xi = []
        # with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/Xi.csv') as f:
        #     reader = csv.reader(f)
        #     for row in reader:
        #         del row[-1]
        #         xi.append(np.array(row, dtype=np.float64))
        # xi = np.array(xi)
        # print("xi: {}\n".format(xi))

        # W
        theta_sw = []
        with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/W.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                del row[-1]
                theta_sw.append(np.array(row, dtype=np.float64))
        # print("theta_sw: {}\n".format(theta_sw))

        # Φ
        phi = []
        with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/phi.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                del row[-1]
                phi.append(np.array(row, dtype=np.float64))
        phi = np.array(phi)
        # print("phi: {}\n".format(phi))

        # 場所の単語辞書
        with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/W_list.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                pass
            place_name_list = row
            # del place_name_list[-1]
        # print(place_name_list)

        # 物体の単語辞書
        # with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/Object_W_list.csv', 'r') as f:
        #     reader = csv.reader(f)
        #     for row in reader:
        #         pass
        #     object_name_list = row
        # del object_name_list[-1]
        # print(object_name_list)
        return pi, theta_sw, phi, place_name_list

    # def save_data(self, prob, place_name, object_name, place_name_list):
    #     # 推論結果をtxtでまとめて保存
    #     FilePath = "/root/HSR/catkin_ws/src/spco2_boo_problog/data/" + str(object_name)
    #     if not os.path.exists(FilePath):
    #         os.makedirs(FilePath)
    #     with open(FilePath + "/cross_modal_inference_result.txt", "w") as f:
    #         f.write("Result of inference:\n")
    #         f.write("{} = {}\n".format(place_name_list, prob))
    #         f.write("Most likely place name is {}\n".format(place_name))
    #         f.close()
    #
    #     # probLogに活用するためにprobだけcsvで保存
    #     with open(FilePath + "/prob.csv", "w") as f:
    #         writer = csv.writer(f)
    #         writer.writerow(prob)

    def cross_modal_inference(self, prob_w_o):
        pi, theta_sw, phi, place_name_list = self.read_data()

        """
        論理推論や重み平均の確率を考慮したP(i_t | O_t) <P(i_t | w_t) = P(i_t | w_t, O_t)を仮定>
        P(i_t | O_t) = ∑_{w} ( (∫ P(i_t | C_t) P(C_t | w_t) dC_t) * P(w_t | O_t) )
        1. prob = P(w_t | O_t)
        2. P(i_t | C_t) = P(i_t | Φ, C_t)
        3. P(C_t | w_t) = P(w_t | W, C_t) P(C_t | π)
        4. 周辺化させた結果を出力させる
        """

        prob_i_t_list = []

        ## P(i_t | w_t)の計算
        for i in range(len(theta_sw[0])):
            place_name_vector = np.zeros(len(theta_sw[0]))
            np.put(place_name_vector, [i], 1)

            prob_i_t = [0.0 for i in range(len(phi[0]))] # 位置分布のindexリスト作成
            for j in range(len(phi[0])):
                for c in range(pi.size):
                    prob = place_name_vector.dot(theta_sw[c].T) * pi[c] * phi[c][j]
                    # P(o_t | xi_c^s) P(C^s | pi) P (w^s | theta^sw_c^s)
                    prob_i_t[j] += prob

            prob_i_t_r = [float(k) / sum(prob_i_t) for k in prob_i_t] # 正規化
            # print("Result of inference:")
            # print("{}\n".format(prob_i_t_r))

            prob_i_t_list.append(prob_i_t_r)

        # print("P(i_t | w_t): {}".format(prob_i_t_list))


        ## ∑_{w} P(i_t | w_t) P(w_t | o_t)の計算
        prob_i_o = [0.0 for i in range(len(phi[0]))] # 位置分布のindexリスト作成
        for i in range(len(phi[0])):
            for w in range(len(theta_sw[0])):
                prob = prob_w_o[w] * prob_i_t_list[w][i]
                prob_i_o[i] += prob

        prob_i_o_r = [float(k) / sum(prob_i_o) for k in prob_i_o] # 正規化
        print("P(i_t | O_t): {}".format(prob_i_o_r))
        return


if __name__ == "__main__":
    # rospy.init_node('cross_modal_object2place')
    cross_modal = CrossModalObject2Place()
    # cross_modal.word_callback()
    # rospy.spin()
