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

x = np.array([0, 1, 2, 3, 4, 5])

# SpCoSLAMの結果読み込み
y_1 = np.array([2, 1, 3, 1, 1, 1])
# e_1 = np.array([1.0, 0.84, 0.71, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

# Priorの結果読み込み
y_2 = np.array([3, 4, 4, 3, 4, 4])

# SpCoSLAM + Priorの結果読み込み
y_3 = np.array([3, 3, 3, 1, 1, 1])
# e_2 = np.array([1.1, 0.87, 0.52, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

# SpCoSLAM + ProbLogの結果読み込み
y_4 = np.array([1, 1, 1, 1, 1, 1])
#e_3 = np.array([0.58, 0.28, 0.20, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

plt.plot(x, y_1, label="SpCoSLAM", color="blue")
plt.errorbar(x, y_1, markersize=5, marker='o', capthick=1, capsize=5, lw=0.5, ecolor = "blue")
plt.plot(x, y_2, label="Prior", color="brown")
plt.errorbar(x, y_2, markersize=5, marker='o', capthick=1, capsize=5, lw=0.5, ecolor = "brown")
plt.plot(x, y_3, label = "SpCoSLAM + Prior", color = "red")
plt.errorbar(x, y_3, markersize=5, marker='o', capthick=1, capsize=5, lw=0.5, color = "red")
plt.plot(x, y_4, label = "SpCoSLAM + ProbLog (提案手法)", color = "green")
plt.errorbar(x, y_4, markersize=5, marker='o', capthick=1, capsize=5, lw=0.5, color = "green")

plt.legend()
#ax.set_xlabel("学習データ数", fontname="MS Gothic")
#ax.set_ylabel("訪問数", fontname="MS Gothic")
plt.xlabel("学習のためにロボットが訪問した場所の数 [回]")
plt.ylabel("訪問数 [回]")
ax.set_xlim(0, 5)
ax.set_ylim(1, 4)

plt.show()