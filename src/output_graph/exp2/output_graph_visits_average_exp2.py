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
y_1 = np.array([2.83, 1.95, 2.04, 1.63, 1.83, 1.42, 1.42, 1.5, 1.42])
e_1 = np.array([1.07, 1.06, 1.24, 0.90, 1.18, 0.81, 1.22, 0.87, 0.76])

# Priorの結果読み込み
y_2 = np.array([1.75, 2.04, 2.04, 2.04, 1.88, 2, 1.79, 2.13, 1.92])
e_2 = np.array([0.72, 1.14, 1.10, 1.10, 1.01, 1.12, 0.91, 1.17, 0.95])

# SpCoSLAM + Priorの結果読み込み
y_3 = np.array([1.79, 1.58, 1.83, 1.63, 1.54, 1.58, 1.46, 1.54, 1.5])
e_3 = np.array([0.96, 0.86, 1.21, 0.90, 0.96, 1.04, 0.87, 1.04, 0.96])

# SpCoSLAM + ProbLogの結果読み込み
y_4 = np.array([1.63, 1.42, 1.63, 1.54, 1.29, 1.29, 1.46, 1.42, 1.46])
e_4 = np.array([0.56, 1.00, 1.03, 0.76, 0.54, 0.84, 0.96, 0.95, 0.96])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

plt.plot(x, y_1, label="SpCoSLAM", color="blue")
plt.errorbar(x, y_1, yerr=e_1, markersize=5, marker='o', capthick=1, capsize=5, lw=0.5, ecolor = "blue")
plt.plot(x, y_2, label="Prior", color="brown")
plt.errorbar(x, y_2, yerr=e_2, markersize=5, marker='o', capthick=1, capsize=5, lw=0.5, ecolor = "brown")
plt.plot(x, y_3, label = "SpCoSLAM + Prior", color = "red")
plt.errorbar(x, y_3, yerr=e_3, markersize=5, marker='o', capthick=1, capsize=5, lw=0.5, color = "red")
plt.plot(x, y_4, label = "SpCoSLAM + ProbLog (Proposed)", color = "green")
plt.errorbar(x, y_4, yerr=e_4, markersize=5, marker='o', capthick=1, capsize=5, lw=0.5, color = "green")

plt.legend()
#ax.set_xlabel("学習データ数", fontname="MS Gothic")
#ax.set_ylabel("訪問数", fontname="MS Gothic")

# 現場学習における部屋の訪問数 [ヶ所]
plt.xlabel("The number of room visits in learning")

# 物体探索における部屋の訪問数 [ヶ所]
plt.ylabel("The number of room visits in object search")
ax.set_xlim(0, 8)
ax.set_ylim(1, 4)

plt.show()