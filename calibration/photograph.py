#!/usr/bin/env python3
# coding=utf-8
"""
photograph.py
双目相机棋盘拍照程序
"""

import threading

import PyCeleX5
import cv2
import numpy
import pyrealsense2 as rs

celex5 = PyCeleX5.PyCeleX5()
realsense = rs.pipeline()


def get_celex5():
    return celex5.getFullPicBuffer()


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
        event_show = get_celex5()
        event_show = cv2.resize(event_show, (480, 300))
        cv2.imshow("event", event_show)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        color_show, _ = get_d435i()
        color_show = cv2.resize(color_show, (480, 270))
        cv2.imshow("color", color_show)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    celex5.openSensor()
    celex5.isSensorReady()
    celex5.setSensorFixedMode(PyCeleX5.CeleX5Mode.Full_Picture_Mode)
    celex5.setFpnFile("FPN_lab.txt")
    celex5.setRotateType(2)

    config = rs.config()
    config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 60)
    config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 60)
    profile = realsense.start(config)
    device = profile.get_device()
    color_sensor = device.query_sensors()[1]
    color_sensor.set_option(rs.option.enable_auto_exposure, False)
    color_sensor.set_option(rs.option.exposure, 156)
    align = rs.align(rs.stream.color)

    threading.Thread(target=show_img, name="Thread-show").start()

    i = 1
    while i < 500:
        name = input()
        if name != "":
            i = int(name)
        event = get_celex5()
        color, depth = get_d435i()
        cv2.imwrite("celex5_{:02d}.png".format(i), event)
        cv2.imwrite("d435i_{:02d}.png".format(i), color)
        numpy.save("depth_{:02d}".format(i), depth)
        print("save {:02d} successful".format(i))
        i = i + 1
