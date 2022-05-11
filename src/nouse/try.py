#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import itertools
import numpy as np

# save_data = [["living", "bedroom", "kitchen"], [0.1, 0.2, 0.3]]
# with open ("/root/HSR/catkin_ws/src/spco2_boo_problog/data/penguin_doll/inference_result.csv", "w") as f:
#     write = csv.writer(f)
#     write.writerows(list(itertools.zip_longest(*save_data, fillvalue='')))
#
# with open("/root/HSR/catkin_ws/src/spco2_boo_problog/data/penguin_doll/inference_result.csv", 'r') as csv_file:
#     csv_reader = csv.reader(csv_file)
#     # Passing the cav_reader object to list() to get a list of lists
#     list_of_rows = list(csv_reader)
#     print(list_of_rows)

phi = []
with open('/root/HSR/catkin_ws/src/spco2_boo_problog/src/param/phi.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        del row[-1]
        phi.append(np.array(row, dtype=np.float64))
phi = np.array(phi)
print(len(phi))