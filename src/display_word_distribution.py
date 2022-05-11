#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library
import csv
import os

# Third Party
import numpy as np
import roslib.packages
import rospy
from std_msgs.msg import String


class DisplayWordDistribution():
    def __init__(self):
        self.cross_modal_inference()

    # def word_callback(self):
    # word = rospy.wait_for_message("/human_command", String, timeout=None)
    # target_name = word.data
    # target_name = object_name
    # print(target_name)
    # target_name = "cup"
    # return prob

    def read_data(self):
        ## データの読み込み
        # π
        with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/pi.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                pass
        pi_s_data = row
        del pi_s_data[-1]
        pi = np.array(pi_s_data, dtype=np.float64)
        # print("pi_s :{}\n".format(pi))

        # Φ
        phi = []
        with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/phi.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                del row[-1]
                phi.append(np.array(row, dtype=np.float64))
        phi = np.array(phi)
        # print("phi: {}\n".format(xi))

        # W
        w = []
        with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/W.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                del row[-1]
                w.append(np.array(row, dtype=np.float64))
        # print("theta_sw: {}\n".format(theta_sw))

        # 場所の単語辞書
        with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/W_list.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                pass
            place_name_list = row
            # del place_name_list[-1]
        # print(place_name_list)

        # ガウス分布の平均値を読み込む
        ####################################

        ####################################

        return pi, phi, w, place_name_list

    def cross_modal_inference(self):
        pi, phi, w, place_name_list = self.read_data()

        """
        P(w_t | i_t)の計算
        P(w_t | i_t) = ∫ P(w_t | C_t) P(C_t | i_t) dC_t
        1. P(C_t | i_t) = P(C_t | π, i_t, Φ) = P(C_t | π) P(i_t | Φ, C_t)
        2. P(w_t | C_t, W)
        3. 周辺化した上で結果を出力させる
        すべての位置分布のindexに対して同様の計算を行う
        """

        for i in range(len(phi[0])):
            position_index_vector = np.zeros(len(phi[0]))
            np.put(position_index_vector, [i], 1)

            prob_w_t = [0.0 for i in range(len(w[0]))]  # 場所の単語リスト作成
            for j in range(len(w[0])):
                for c in range(pi.size):
                    prob = position_index_vector.dot(phi[c].T) * pi[c] * w[c][j]
                    # P(i_t | phi_c) P(C_t | pi) P (w_t | W_c)
                    prob_w_t[j] += prob

            prob_w_s_t_r = [float(k) / sum(prob_w_t) for k in prob_w_t]  # 正規化
            prob_w_t = [round(prob_w_s_t_r[n], 3) for n in range(len(prob_w_s_t_r))] # 小数点2桁

            print("Result of inference:")
            print("{}\n".format(place_name_list))
            print("{}\n".format(prob_w_t))


            w_t_1 = sorted(prob_w_s_t_r)[-1]
            w_t_2 = sorted(prob_w_s_t_r)[-2]
            w_t_3 = sorted(prob_w_s_t_r)[-3]
            w_t_4 = sorted(prob_w_s_t_r)[-4]

            print("1st highest probability: {} = {:.3f}\n".format(place_name_list[prob_w_s_t_r.index(w_t_1)], w_t_1))
            print("2nd highest probability: {} = {:.3f}\n".format(place_name_list[prob_w_s_t_r.index(w_t_2)], w_t_2))
            print("3rd highest probability: {} = {:.3f}\n".format(place_name_list[prob_w_s_t_r.index(w_t_3)], w_t_3))
            print("4th highest probability: {} = {:.3f}\n".format(place_name_list[prob_w_s_t_r.index(w_t_4)], w_t_4))

            print(len(place_name_list))
            print("********************************************************")

            # 位置分布のindexに対応するガウスの平均値を読み込む
            # 伊藤が作ったrosのmsgに格納し、publish

        return


if __name__ == "__main__":
    rospy.init_node('word')
    display_word_distribution = DisplayWordDistribution()
    # cross_modal.word_callback()
    rospy.spin()
