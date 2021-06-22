#!/usr/bin/env python3
# coding=utf-8
"""
verified_to_raw.py
已验证标签转为原始标签程序
"""
import os
import shutil

ROOT_PATH = r"Y:\ZJUT\temp"


def remove_line(file: str):
    with open(file, "r") as f:
        data = f.readlines()
    data.pop(1)
    with open(file, "w") as f:
        f.writelines(data)


for person in os.listdir(ROOT_PATH):
    p_path = os.path.join(ROOT_PATH, person)
    for s in os.listdir(p_path):
        s_path = os.path.join(p_path, s)
        label_color = os.path.join(s_path, "label_color")
        label_color_fill = os.path.join(s_path, "label_color_fill")
        label_event = os.path.join(s_path, "label_event")
        label_event_fill = os.path.join(s_path, "label_event_fill")
        shutil.rmtree(label_color)
        shutil.rmtree(label_event)
        shutil.move(label_color_fill, label_color)
        shutil.move(label_event_fill, label_event)
        for file in os.listdir(label_color):
            remove_line(os.path.join(label_color, file))
        for file in os.listdir(label_event):
            remove_line(os.path.join(label_event, file))
