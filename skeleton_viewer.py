#!/usr/bin/env python3
# coding=utf-8
"""
skeleton_viewer.py
快速可视化图片及骨架
"""
import os

import cv2
import numpy

ROOT_PATH = r"Y:\ZJUT\Verified\A0025P0017\S00"

RED = (0, 0, 255)
GREEN = (0, 255, 0)
COLOR_LIST = [RED] * 7 + [GREEN] * 7
SKELETON = [[0, 1], [1, 3], [3, 5], [1, 7], [1, 2], [7, 9], [9, 11],
            [0, 2], [2, 4], [4, 6], [2, 8], [7, 8], [8, 10], [10, 12]]


def show_skeleton(root_path: str):
    color_label_path = os.path.join(ROOT_PATH, "label_color_fill")
    event_label_path = os.path.join(ROOT_PATH, "label_event_fill")
    if not os.path.exists(color_label_path):
        print("color label not exists: " + color_label_path)
        return
    if not os.path.exists(event_label_path):
        print("event label not exists: " + event_label_path)
    colors = os.listdir(color_label_path)
    events = os.listdir(event_label_path)
    if len(colors) != len(events):
        print("file count not same: color {}, event {}".format(len(colors), len(events)))

    colors.sort()
    events.sort()
    for i in range(len(colors)):
        color = cv2.imread(os.path.join(root_path, "color", colors[i][0: -4] + ".png"))
        color_label = load_label(os.path.join(color_label_path, colors[i]), "color")
        color = add_skeleton(color, color_label)
        color = cv2.resize(color, (960, 540))
        cv2.imshow("color", color)
        cv2.waitKey(1)

        event = cv2.imread(os.path.join(root_path, "image_event_binary", events[i][0: -4] + ".png"))
        event_label = load_label(os.path.join(event_label_path, events[i]), "event")
        event = add_skeleton(event, event_label)
        event = cv2.resize(event, (960, 600))
        cv2.imshow("event", event)
        cv2.waitKey(1)


def load_label(label_path: str, label_type: str):
    with open(label_path) as f:
        data = f.read().split("\n")
    result = []
    if data[0] != "13":
        print("wrong keypoint count: {}, {}".format(label_path, data[0]))
        return result
    for point in data[2:-1]:
        point = point.split(" ")
        if label_type == "event":
            result.append([round(float(point[0][1:-1])), round(float(point[1][1:-1]))])
        elif label_type == "color":
            result.append([float(point[0]) * 848, float(point[1]) * 480])
    return numpy.array(result)


def add_skeleton(image, key_points):
    if len(key_points) != 13:
        return image
    for i, keypoint in enumerate(SKELETON):
        p1 = (int(key_points[keypoint[0], 0]), int(key_points[keypoint[0], 1]))
        p2 = (int(key_points[keypoint[1], 0]), int(key_points[keypoint[1], 1]))
        cv2.line(image, p1, p2, COLOR_LIST[i], 2, 8)
    return image


if __name__ == "__main__":
    show_skeleton(ROOT_PATH)
