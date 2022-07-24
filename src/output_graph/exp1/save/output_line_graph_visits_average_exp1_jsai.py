#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns
import numpy as np
from matplotlib.legend import Legend
import pandas as pd


#plt.style.use('default')
sns.set()
sns.set_style("whitegrid", {'grid.linestyle': '--'})
sns.set_context("paper", 1, {"lines.linewidth": 1})
#sns.set_palette('Set1')
japanize_matplotlib.japanize()

x = np.array([0, 1, 2, 3, 4, 5])

# SpCoSLAMの結果読み込み
y_1 = np.array([2.5, 1.83, 2.0, 1.0, 1.0, 1.0])
e_1 = np.array([0.96, 0.85, 0.82, 0.0, 0.0, 0.0])

# Priorの結果読み込み
y_2 = np.array([1.83, 1.96, 1.83, 1.83, 1.96, 1.79])
e_2 = np.array([0.94, 1.06, 1.03, 0.94, 0.98, 0.96])

# SpCoSLAM + Priorの結果読み込み
y_3 = np.array([1.88, 1.29, 1.46, 1.0, 1.0, 1.0])
e_3 = np.array([0.93, 0.61, 0.76, 0.0, 0.0, 0.0])

# SpCoSLAM + ProbLogの結果読み込み
y_4 = np.array([1.42, 1.04, 1.04, 1.0, 1.0, 1.0])
e_4 = np.array([0.49, 0.20, 0.20, 0.0, 0.0, 0.0])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

plt.plot(x, y_1, label='SpCoSLAM', color='green', marker='.', markersize=5, linestyle='solid', linewidth=1.5)
# plt.errorbar(x, y_1, yerr=e_1, markersize=5, marker='o', capthick=1, capsize=7, lw=1, ecolor = "blue")
ax.fill_between(x, y_1 + e_1, y_1 - e_1, facecolor='green', alpha=0.1)

plt.plot(x, y_2, label="Prior", color="brown", marker='.', markersize=5, linestyle='solid', linewidth=1.5)
# plt.errorbar(x, y_2, yerr=e_2, markersize=5, marker='o', capthick=1, capsize=7, lw=1, ecolor = "brown")
ax.fill_between(x, y_2 + e_2, y_2 - e_2, facecolor='brown', alpha=0.1)

plt.plot(x, y_3, label = "SpCoSLAM + Prior", color = "red", marker='.', markersize=5, linestyle='solid', linewidth=1.5)
# plt.errorbar(x, y_3, yerr=e_3, markersize=5, marker='o', capthick=1, capsize=7, lw=1, color = "red")
ax.fill_between(x, y_3 + e_3, y_3 - e_3, facecolor='red', alpha=0.1)

plt.plot(x, y_4, label = "SpCoSLAM + ProbLog (Proposed)", color="blue", marker='.', markersize=5, linestyle='solid', linewidth=3)
# plt.errorbar(x, y_4, yerr=e_4, markersize=5, marker='o', capthick=1, capsize=7, lw=1, color = "green")
ax.fill_between(x, y_4 + e_4, y_4 - e_4, facecolor='blue', alpha=0.2)

plt.legend()


# 現場学習における部屋の訪問数 [ヶ所]
plt.xlabel("学習における部屋の訪問数 [ヶ所]")

# 物体探索における部屋の訪問数 [ヶ所]
plt.ylabel("探索における部屋の訪問数 [ヶ所]")
ax.set_xlim(0, 5)
ax.set_ylim(1, 4)

plt.show()