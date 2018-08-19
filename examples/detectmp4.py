# Stupid python path shit.
# Instead just add darknet.py to somewhere in your python path
# OK actually that might not be a great idea, idk, work in progress
# Use at your own risk. or don't, i don't care


from scipy.misc import imread
import cv2

def array_to_image(arr):
    arr = arr.transpose(2,0,1)
    c = arr.shape[0]
    h = arr.shape[1]
    w = arr.shape[2]
    arr = (arr/255.0).flatten()
    data = dn.c_array(dn.c_float, arr)
    im = dn.IMAGE(w,h,c,data)
    return im

def detect2(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    boxes = dn.make_boxes(net)
    probs = dn.make_probs(net)
    num =   dn.num_boxes(net)
    dn.network_detect(net, image, thresh, hier_thresh, nms, boxes, probs)
    res = []
    for j in range(num):
        for i in range(meta.classes):
            if probs[j][i] > 0:
                res.append((meta.names[i], probs[j][i], (boxes[j].x, boxes[j].y, boxes[j].w, boxes[j].h)))
    res = sorted(res, key=lambda x: -x[1])
    dn.free_ptrs(dn.cast(probs, dn.POINTER(dn.c_void_p)), num)
    return res

import sys, os
sys.path.append(os.path.join(os.getcwd(),'python/'))

import darknet as dn
print dn.__dict__

# Darknet
DARKNET_DIR="/mnt/c/Users/sakak/workspace/darknet/"
DARKNET_CFG,DARKNET_WEIGHTS,DARKNET_DATA= DARKNET_DIR+"cfg/yolov3.cfg",DARKNET_DIR+"yolov3.weights",DARKNET_DIR+"cfg/coco.data"

net = dn.load_net(DARKNET_CFG,DARKNET_WEIGHTS,0)
meta = dn.load_meta(DARKNET_DATA)

VIDEO_NAME="some video name"
cap=cv2.VideoCapture(VIDEO_NAME)
while cap.isOpened():
    ret,frame=cap.read()
    if ret:
#        video.append(frame)
        cv2.imwrite(VIDEO_NAME+'/frame'+count+'.mp4')
        im=array_to_image(frame)
        dn.rgbgr_image(im)
        r = detect2(net, meta, im)
        print r
    else:
        break
    count+=1
cap.release()

