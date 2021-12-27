#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import numpy as np

theta_sw = []
with open('/root/HSR/W.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        del row[-1]
        theta_sw.append(np.array(row, dtype=np.float64))

print("theta_sw: {}".format(theta_sw))
theta_sw = np.array(theta_sw)
data = np.array([1, 0, 0, 0])
prob = data.dot(theta_sw[0].T)
print(prob)

