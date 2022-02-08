#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns
import numpy as np
import pandas as pd


#plt.style.use('default')
sns.set()
sns.set_style("whitegrid", {'grid.linestyle': '--'})
sns.set_context("paper", 1, {"lines.linewidth": 1})
#sns.set_palette('Set1')
japanize_matplotlib.japanize()

x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])

# SpCoSLAMの結果読み込み
y_1 = np.array([0.25, 0.30, 0.30, 0.48, 0.74, 0.80, 0.82, 0.85, 0.86])
# e_1 = np.array([1.0, 0.84, 0.71, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

# SpCoSLAM + Priorの結果読み込み
y_2 = np.array([0.23, 0.27, 0.27, 0.42, 0.64, 0.68, 0.70, 0.72, 0.74])
# e_2 = np.array([1.1, 0.87, 0.52, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

# SpCoSLAM + ProbLogの結果読み込み
y_3 = np.array([0.25, 0.29, 0.29, 0.44, 0.66, 0.7, 0.72, 0.74, 0.76])
#e_3 = np.array([0.58, 0.28, 0.20, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

plt.plot(x, y_1, label="SpCoSLAM (ベースライン手法1)", color="blue")
plt.errorbar(x, y_1, markersize=5, marker='o', capthick=1, capsize=5, lw=0.5, ecolor = "blue")
plt.plot(x, y_2, label = "SpCoSLAM + Prior (ベースライン手法2)", color = "red")
plt.errorbar(x, y_2, markersize=5, marker='o', capthick=1, capsize=5, lw=0.5, color = "red")
plt.plot(x, y_3, label = "SpCoSLAM + ProbLog (提案手法)", color = "green")
plt.errorbar(x, y_3, markersize=5, marker='o', capthick=1, capsize=5, lw=0.5, color = "green")

plt.legend()
#ax.set_xlabel("学習データ数", fontname="MS Gothic")
#ax.set_ylabel("訪問数", fontname="MS Gothic")
plt.xlabel("現場学習における部屋の訪問数 [ヶ所]")
plt.ylabel("実際に対象物が存在する場所に対する推論時の確率値")
ax.set_xlim(0, 8)
ax.set_ylim(0, 1)
plt.yticks( np.arange(0, 1.1, 0.1) )

plt.show()