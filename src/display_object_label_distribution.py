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


class DisplayObjectLabelDistribution():
    def __init__(self):
        self.cross_modal_inference()


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
        # print("phi: {}\n".format(phi))

        # ξ
        xi = []
        with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/Xi.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                del row[-1]
                xi.append(np.array(row, dtype=np.float64))
        xi = np.array(xi)
        # print("xi: {}\n".format(xi))


        # 物体の単語辞書
        with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/Object_W_list.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                pass
            object_name_list = row


        # ガウス分布の平均値を読み込む
        ####################################

        ####################################

        return pi, phi, xi, object_name_list


    def cross_modal_inference(self):
        pi, phi, xi, object_name_list = self.read_data()

        """
        P(O_t | i_t)の計算
        P(O_t | i_t) = ∫ P(O_t | C_t) P(C_t | i_t) dC_t
        1. P(C_t | i_t) = P(C_t | π, i_t, Φ) = P(C_t | π) P(i_t | Φ, C_t)
        2. P(O_t | C_t, ξ)
        3. 周辺化した上で結果を出力させる
        すべての位置分布のindexに対して同様の計算を行う
        """

        for i in range(len(phi[0])):
            position_index_vector = np.zeros(len(phi[0]))
            np.put(position_index_vector, [i], 1)

            prob_o_t = [0.0 for i in range(len(xi[0]))]  # 場所の単語リスト作成
            for j in range(len(xi[0])):
                for c in range(pi.size):
                    prob = position_index_vector.dot(phi[c].T) * pi[c] * xi[c][j]
                    # P(i_t | phi_c) P(C_t | pi) P (O_t | xi_c)
                    prob_o_t[j] += prob

            prob_o_t_r = [float(k) / sum(prob_o_t) for k in prob_o_t]  # 正規化
            prob_o_t = [round(prob_o_t_r[n], 3) for n in range(len(prob_o_t_r))] # 小数点2桁

            print("Result of inference:")
            print("{}\n".format(object_name_list))
            print("{}\n".format(prob_o_t))

            o_t_1 = sorted(prob_o_t_r)[-1]
            o_t_2 = sorted(prob_o_t_r)[-2]
            o_t_3 = sorted(prob_o_t_r)[-3]
            o_t_4 = sorted(prob_o_t_r)[-4]

            print("1st highest probability: {} = {:.3f}\n".format(object_name_list[prob_o_t_r.index(o_t_1)], o_t_1))
            print("2nd highest probability: {} = {:.3f}\n".format(object_name_list[prob_o_t_r.index(o_t_2)], o_t_2))
            print("3rd highest probability: {} = {:.3f}\n".format(object_name_list[prob_o_t_r.index(o_t_3)], o_t_3))
            print("4th highest probability: {} = {:.3f}\n".format(object_name_list[prob_o_t_r.index(o_t_4)], o_t_4))

            print("********************************************************")

            # o_t = np.argmax(prob_o_t_r)
            # print("Most likely object is {}\n".format(object_name_list[o_t], o_t))

            # 位置分布のindexに対応するガウスの平均値を読み込む
            # 伊藤が作ったrosのmsgに格納し、publish

        return

if __name__ == "__main__":
    rospy.init_node('word')
    display_word_distribution = DisplayObjectLabelDistribution()
    # cross_modal.word_callback()
    # rospy.spin()


