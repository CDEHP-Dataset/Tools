#!/usr/bin/env python3
# coding=utf-8
"""
label_reverse.py
左右部件交换程序
"""
import os

ROOT_PATH = r"T:\te"

for file in os.listdir(ROOT_PATH):
    new_name = file + ".bk"
    old_path = os.path.join(ROOT_PATH, file)
    new_path = os.path.join(ROOT_PATH, new_name)
    os.rename(old_path, new_path)
    with open(new_path, "r") as f:
        data = f.readlines()
    data[2], data[3] = data[3], data[2]
    data[4], data[5] = data[5], data[4]
    data[6], data[7] = data[7], data[6]
    data[8], data[9] = data[9], data[8]
    data[10], data[11] = data[11], data[10]
    data[12], data[13] = data[13], data[12]
    with open(old_path, "w") as f:
        f.writelines(data)
