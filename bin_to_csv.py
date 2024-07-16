#!/usr/bin/env python3
# coding=utf-8
"""
bin_to_picture.py
将Bin文件导出Event数据
Export the event data from Bin files
"""
import os
import time

import PyCeleX5

ROOT_PATH = "/home/datasets/ZJUT/Source/"
FRAME_TIME = 8333

celex5 = PyCeleX5.PyCeleX5(debug=False)
celex5.setRotateType(2)
celex5.setEventFrameTime(FRAME_TIME)

bin_files = []
for datasets in os.listdir(ROOT_PATH):
    dataset_path = os.path.join(ROOT_PATH, datasets)
    for ap in os.listdir(dataset_path):
        ap_path = os.path.join(dataset_path, ap)
        for s in os.listdir(ap_path):
            s_path = os.path.join(ap_path, s)
            event = os.path.join(s_path, "event")
            vector_event_binary = os.path.join(s_path, "vector_event_binary")
            if not os.path.exists(event) or len(os.listdir(event)) != 1 or not os.listdir(event)[0].endswith(".bin"):
                print("{} don't have event file".format(s_path))
                continue
            if os.path.exists(vector_event_binary):
                print("{} already have vector event".format(s_path))
                continue
            bin_files.append(s_path)

for file in bin_files:
    event = os.path.join(file, "event")
    vector_event_binary = os.path.join(file, "vector_event_binary")
    os.mkdir(vector_event_binary)
    bin = os.listdir(event)[0]
    bin_name = bin[0:bin.find(".")]
    source = os.path.join(event, bin)
    target = os.path.join(vector_event_binary, bin_name + ".csv")

    celex5.startRippingBinFile()
    celex5.enableEventDataOutput(target)
    celex5.openBinFile(source)
    while not celex5.readBinFileData() or not celex5.rippingBinFileFinished():
        pass
    time.sleep(10)
    celex5.stopRippingBinFile()
    print("Ripping {} done".format(file))
print("All done")
