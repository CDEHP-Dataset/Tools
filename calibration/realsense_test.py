#!/usr/bin/env python3
# coding=utf-8
"""
realsense_test.py
深度相机测试程序
"""
import threading

import cv2
import numpy
import pyrealsense2 as rs

realsense = rs.pipeline()


def get_d435i():
    while True:
        frames = realsense.wait_for_frames()
        aligned_frames = align.process(frames)
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        if color_frame and depth_frame:
            break
    color_image = numpy.asanyarray(color_frame.get_data())
    depth_image = numpy.asanyarray(depth_frame.get_data())
    return color_image, depth_image


def show_img():
    while True:
        color_show, _ = get_d435i()
        color_show = cv2.resize(color_show, (480, 270))
        cv2.imshow("color", color_show)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    config = rs.config()
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config.enable_record_to_file("T:\\test.bag")
    profile = realsense.start(config)
    align = rs.align(rs.stream.color)

    recorder = realsense.get_active_profile().get_device()
    recorder.as_recorder()

    threading.Thread(target=show_img, name="Thread-show").start()

    text = input()
    recorder.pause()
    text = input()
    recorder.resume()
    text = input()
    realsense.stop()
