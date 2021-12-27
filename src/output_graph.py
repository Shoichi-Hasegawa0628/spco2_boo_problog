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

x = np.array([0, 20, 40, 60, 80])

# SpCoSLAMの結果読み込み
y_1 = np.array([2.3, 1.5, 1.3, 1.3, 1.0])
e_1 = np.array([1.0, 0.65, 0.49, 0.47, 0.0])
# SpCoSLAM + ProbLogの結果読み込み
y_2 = np.array([1.5, 1.3, 1.2, 1.0, 1.0])
e_2 = np.array([0.33, 0.62, 0.37, 0.2, 0.0])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

plt.plot(x, y_1, label="SpCoSLAM", color="blue")
plt.errorbar(x, y_1, yerr=e_1, markersize=5, marker='o', capthick=1, capsize=10, lw=1, ecolor = "blue")
plt.plot(x, y_2, label = "SpCoSLAM + ProbLog", color = "red")
plt.errorbar(x, y_2, yerr=e_2, markersize=5, marker='o', capthick=1, capsize=10, lw=1, color = "red")

plt.legend()
#ax.set_xlabel("学習データ数", fontname="MS Gothic")
#ax.set_ylabel("訪問数", fontname="MS Gothic")
plt.xlabel("学習データ数")
plt.ylabel("訪問数(平均値)")
#ax.set_xlim(0, 80)
ax.set_ylim(1, 4)

plt.show()