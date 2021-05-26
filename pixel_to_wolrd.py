#!/usr/bin/env python3
# coding=utf-8
"""
pixel_to_wolrd.py
给定像素坐标计算已相机为原点的世界坐标
"""

import json
import os

import numpy
import pyrealsense2 as rs


class CoordinateConverter:
    def __init__(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError("depth image not found")
        self.data = numpy.load(path)
        with open("./intrinsics.json") as f:
            intrinsics = json.load(f)
        self.intrinsics = rs.intrinsics()
        self.intrinsics.width = intrinsics["depth"]["width"]
        self.intrinsics.height = intrinsics["depth"]["height"]
        self.intrinsics.fx = intrinsics["depth"]["fx"]
        self.intrinsics.fy = intrinsics["depth"]["fy"]
        self.intrinsics.ppx = intrinsics["depth"]["ppx"]
        self.intrinsics.ppy = intrinsics["depth"]["ppy"]
        self.intrinsics.coeffs = intrinsics["depth"]["coeffs"]
        self.depth_scale = intrinsics["depth_scale"]

    def convert(self, x: int, y: int):
        distance = self.data[x][y] * self.depth_scale
        camera_coordinate = rs.rs2_deproject_pixel_to_point(self.intrinsics, [x, y], distance)
        return camera_coordinate


def main():
    img = "T:\\test.npy"
    converter = CoordinateConverter(img)
    print(converter.convert(2, 3))
    print(converter.convert(4, 6))


main()
