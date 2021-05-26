# Perry25数据集

* 标定
* 拍摄
* 转录
* 标注

## OpenCV

```bash
sudo su root
apt install build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev python3-dev python3-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev

cd /usr/local/src
wget https://github.com/opencv/opencv/archive/refs/tags/3.3.0.tar.gz -O opencv_3.3.0.tar.gz
wget https://github.com/opencv/opencv_contrib/archive/refs/tags/3.3.0.tar.gz -O opencv_contrib_3.3.0.tar.gz
tar -xzvf opencv_3.3.0.tar.gz
tar -xzvf opencv_contrib_3.3.0.tar.gz
cd opencv-3.3.0/

sed -i "1i\#define AV_CODEC_FLAG_GLOBAL_HEADER (1 << 22)" modules/videoio/src/cap_ffmpeg_impl.hpp
sed -i "2i\#define CODEC_FLAG_GLOBAL_HEADER AV_CODEC_FLAG_GLOBAL_HEADER" modules/videoio/src/cap_ffmpeg_impl.hpp
sed -i "3i\#define AVFMT_RAWPICTURE 0x0020" modules/videoio/src/cap_ffmpeg_impl.hpp
sed -i "854s/PyString/(char *)PyString/" modules/python/src2/cv2.cpp

mkdir build
cd build/
cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local/ -D OPENCV_EXTRA_MODULES=../../opencv_contrib-3.3.0/modules/ -D BUILD_DOCS=ON -D BUILD_EXAMPLES=ON -D WITH_CUDA=OFF ..
make -j8
make install

ldconfig /usr/local/lib
```

## 标定

1. 使用`calibration/save_intrinsics.py`程序获取深度相机内参
2. 使用`CelePixel/Calibration-Tools`程序在线拍摄标定事件相机内参
3. `MATLAB`打印棋盘`open checkerboardPattern.pdf`，打印时选择实际大小，方格长度应为`23mm`
4. 同时拍摄深度相机、事件相机
5. 打开两个`Camera Calibrator`程序，畸变参数`Radial Distortion`设为三参数`3 Coefficients`
6. 分别标定深度相机、事件相机，去除无法识别和部分识别的图片，保持两者一致
7. 导出坐标点
8. 计算
