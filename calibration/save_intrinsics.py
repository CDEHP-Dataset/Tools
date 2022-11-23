#!/usr/bin/env python3
# coding=utf-8
"""
save_intrinsics.py
保存RealSense内参
"""

import json

import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 60)
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 60)
profile = pipeline.start(config)
align = rs.align(rs.stream.color)

frames = pipeline.wait_for_frames()
aligned_frames = align.process(frames)
depth_frame = aligned_frames.get_depth_frame()
color_frame = aligned_frames.get_color_frame()
color_intrinsics = color_frame.profile.as_video_stream_profile().intrinsics
depth_intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
camera_intrinsics = {"color": {"width": color_intrinsics.width, "height": color_intrinsics.height,
                               "fx": color_intrinsics.fx, "fy": color_intrinsics.fy,
                               "ppx": color_intrinsics.ppx, "ppy": color_intrinsics.ppy,
                               "coeffs": color_intrinsics.coeffs},
                     "depth": {"width": depth_intrinsics.width, "height": depth_intrinsics.height,
                               "fx": depth_intrinsics.fx, "fy": depth_intrinsics.fy,
                               "ppx": depth_intrinsics.ppx, "ppy": depth_intrinsics.ppy,
                               "coeffs": depth_intrinsics.coeffs},
                     "depth_scale": profile.get_device().first_depth_sensor().get_depth_scale()}
with open("../../intrinsics.json", "w") as f:
    json.dump(camera_intrinsics, f)

print("done")
