#!/usr/bin/env python3
# coding=utf-8
"""
bin_to_picture.py
将Bin文件转录为图片序列
"""
import os
import time

import PyCeleX5

ROOT_PATH = "/home/datasets/ZJUT/"
FRAME_TIME = 8333

celex5 = PyCeleX5.PyCeleX5(debug=False)
celex5.setRotateType(2)
celex5.setEventFrameTime(FRAME_TIME)

bin_files = []
for ap in os.listdir(ROOT_PATH):
    ap_path = os.path.join(ROOT_PATH, ap)
    for s in os.listdir(ap_path):
        path = os.path.join(ap_path, s, "event")
        files = os.listdir(path)
        if len(files) == 1 and files[0].endswith(".bin"):
            bin_files.append(os.path.join(path, files[0]))

# TODO 多线程解析

celex5.startRippingBinFile()
for file in bin_files:
    path = os.path.dirname(file) + os.sep
    celex5.setRippingPath(path)
    celex5.openBinFile(file)
    while not celex5.readBinFileData():
        pass
    count = len(os.listdir(path))
    # 保证=所有图片都已保存完
    while True:
        time.sleep(1)
        new_count = len(os.listdir(path))
        if count != new_count:
            count = new_count
        else:
            break
    print("ripping {} done, generate {} images".format(file, count - 1))
    time.sleep(1)

celex5.stopRippingBinFile()
