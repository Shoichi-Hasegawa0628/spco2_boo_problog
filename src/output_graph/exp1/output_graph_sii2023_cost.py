#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
# import matplotlib

# import japanize_matplotlib
import seaborn as sns
import numpy as np
from matplotlib.legend import Legend
import pandas as pd

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42


#plt.style.use('default')
# sns.set()
# sns.set_style("whitegrid", {'grid.linestyle': '--'})
# sns.set_context("paper", 1, {"lines.linewidth": 1})
#sns.set_palette('Set1')
# japanize_matplotlib.japanize()

x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

# SpCoSLAMの結果読み込み
y_1 = np.array([0.33, 0.13, 0.46, 0.46, 0.54, 0.54, 0.54, 0.54, 0.83, 0.67, 0.83, 0.83, 0.96])
# e_1 = np.array([1.18, 0.95, 1.06, 1.06, 1.07, 1.00, 1.31, 0.97, 0.80, 0.56, 0.50, 0.50, 0.20])

# Priorの結果読み込み
y_2 = np.array([0.50, 0.54, 0.50, 0.50, 0.50, 0.42, 0.46, 0.46, 0.50, 0.50, 0.42, 0.38, 0.42])
# e_2 = np.array([0.96, 0.97, 0.96, 1.03, 0.96, 1.00, 0.94, 1.01, 1.00, 1.03, 0.85, 1.04, 0.93])

# SpCoSLAM + Priorの結果読み込み
y_3 = np.array([0.50, 0.38, 0.63, 0.71, 0.63, 0.75, 0.75, 0.67, 0.92, 0.83, 0.92, 0.92, 1.00])
# e_3 = np.array([1.00, 1.00, 0.82, 0.63, 0.76, 0.76, 0.62, 0.91, 0.44, 0.37, 0.28, 0.44, 0.00])

# SpCoSLAM + ProbLogの結果読み込み
y_4 = np.array([0.54, 0.50, 0.71, 0.67, 0.75, 0.88, 0.79, 0.79, 0.92, 0.92, 0.88, 0.92, 1.00])
# e_4 = np.array([0.58, 0.96, 0.45, 0.87, 0.43, 0.66, 0.41, 0.52, 0.44, 0.44, 0.83, 0.44, 0.00])

# 満足基準
y_5 = np.array([0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

plt.plot(x, y_1, label='SpCoSLAM', color='green', marker='.', markersize=5, linestyle='solid', linewidth=1.5)
# plt.errorbar(x, y_1, yerr=e_1, markersize=5, marker='o', capthick=1, capsize=7, lw=1, ecolor = "blue")
# ax.fill_between(x, y_1 + e_1, y_1 - e_1, facecolor='green', alpha=0.1)

plt.plot(x, y_2, label="Prior", color="brown", marker='.', markersize=5, linestyle='solid', linewidth=1.5)
# plt.errorbar(x, y_2, yerr=e_2, markersize=5, marker='o', capthick=1, capsize=7, lw=1, ecolor = "brown")
# ax.fill_between(x, y_2 + e_2, y_2 - e_2, facecolor='brown', alpha=0.1)

plt.plot(x, y_3, label = "SpCoSLAM + Prior", color = "red", marker='.', markersize=5, linestyle='solid', linewidth=1.5)
# plt.errorbar(x, y_3, yerr=e_3, markersize=5, marker='o', capthick=1, capsize=7, lw=1, color = "red")
# ax.fill_between(x, y_3 + e_3, y_3 - e_3, facecolor='red', alpha=0.1)

plt.plot(x, y_4, label = "SpCoSLAM + ProbLog (Proposed)", color="blue", marker='.', markersize=5, linestyle='solid', linewidth=2.5)
# plt.errorbar(x, y_4, yerr=e_4, markersize=5, marker='o', capthick=1, capsize=7, lw=1, color = "green")
# ax.fill_between(x, y_4 + e_4, y_4 - e_4, facecolor='blue', alpha=0.1)

plt.plot(x, y_5, label = "Satisfaction threshold", color="deepskyblue", marker='.', markersize=5, linestyle='dotted', linewidth=2.5)

plt.legend()


# 現場学習における部屋の訪問数 [ヶ所]
plt.xlabel("The number of room visits in learning")

# 物体探索における部屋の訪問数 [ヶ所]
plt.ylabel("Proportions of objects found by th robot in one search")
ax.set_xlim(0, 12)
ax.set_ylim(0, 1)

plt.savefig("./fig.pdf", bbox_inches="tight")
plt.savefig("./fig.eps", bbox_inches="tight")
plt.savefig("./fig.svg", bbox_inches="tight")
plt.show()