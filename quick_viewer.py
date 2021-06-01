#!/usr/bin/env python3
# coding=utf-8
"""
quick_viewer.py
快速可视化拍摄的图片
"""
import os
import threading

import cv2

ROOT_PATH = "Y:\\ZJUT\\0531"


def show_images(images_path: str, image_type: str):
    images_path = os.path.join(images_path, image_type)
    for file in os.listdir(images_path):
        file_path = os.path.join(images_path, file)
        image = cv2.imread(file_path)
        if image_type == "color":
            image = cv2.resize(image, (480, 270))
        else:
            image = cv2.resize(image, (480, 300))
        cv2.imshow(image_type, image)
        cv2.waitKey(1)
    cv2.destroyWindow(image_type)


def show_multi_streams(image_path: str):
    print("viewing directory {}".format(image_path))
    threading.Thread(target=show_images, args=(image_path, "color"), name="Thread-Color").start()
    threading.Thread(target=show_images, args=(image_path, "image_event_binary"), name="Thread-Event").start()


if __name__ == "__main__":
    directories = []
    for ap in os.listdir(ROOT_PATH):
        ap_path = os.path.join(ROOT_PATH, ap)
        for s in os.listdir(ap_path):
            s_path = os.path.join(ap_path, s)
            if os.path.exists(os.path.join(s_path, "color")) and os.path.exists(
                    os.path.join(s_path, "image_event_binary")):
                directories.append(s_path)
    directories.sort()
    for path in directories:
        show_multi_streams(path)
        command = input()
        while command.strip() != "":
            if command == "r":
                show_multi_streams(path)
            elif os.path.exists(command):
                show_multi_streams(command)
            command = input()
