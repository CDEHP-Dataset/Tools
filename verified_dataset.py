# coding=utf-8
# @Author: 呉真 Kuretru < kuretru@gmail.com >
"""
verified_dataset.py
验证数据集是否完整程序
"""

import os

# ROOT_PATH = "Y:\\ZJUT\\Source\\"
ROOT_PATH = "/home/datasets/ZJUT/Source/"
DIRECTORIES = ["color", "depth_raw", "event", "vector_event_binary", "image_event_binary",
               "label_color", "label_color_fill", "label_event", "label_event_fill"]

for datasets in os.listdir(ROOT_PATH):
    dataset_path = os.path.join(ROOT_PATH, datasets)
    for ap in os.listdir(dataset_path):
        ap_path = os.path.join(dataset_path, ap)
        for s in os.listdir(ap_path):
            s_path = os.path.join(ap_path, s)
            directories = os.listdir(s_path)
            for dir in DIRECTORIES:
                if dir not in directories:
                    print("{} no {}".format(s_path, dir))
print("done")
