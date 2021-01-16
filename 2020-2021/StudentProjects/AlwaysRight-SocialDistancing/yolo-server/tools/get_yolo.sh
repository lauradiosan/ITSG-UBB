#!/bin/bash
echo $1
if [ "$1" == "tiny" ]; then
    wget -O ../resources/yolov3-tiny.weights https://pjreddie.com/media/files/yolov3-tiny.weights
    wget -O ../resources/yolov3-tiny.cfg https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-tiny.cfg
else
    wget -O ../resources/yolov3.weights https://pjreddie.com/media/files/yolov3.weights
    wget -O ../resources/yolov3.cfg https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg
fi

