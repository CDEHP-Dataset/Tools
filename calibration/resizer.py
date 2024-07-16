#!/usr/bin/env python3
# coding=utf-8
"""
resizer.py
将指定目录图片压缩至指定分辨率
resize all the images in a specified directory
"""

import os

import cv2

ROOT_PATH = r"Y:\标定_0517\celex5d"
RESOLUTION = [1280, 720]

os.chdir(ROOT_PATH)
for file in os.listdir():
    img = cv2.imread(file)
    resized = cv2.resize(img, RESOLUTION)
    cv2.imwrite(file, resized)
    print("resize {} successful".format(file))

print("done")
