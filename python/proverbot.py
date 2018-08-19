from darknet import *

DARKNET_DIR="/mnt/c/Users/sakak/workspace/darknet/"

def predict_tactic(net, s):
    prob = 0
    d = c_array(c_float, [0.0]*256)
    tac = ''
    if not len(s):
        s = '\n'
    for c in s[:-1]:
        d[ord(c)] = 1
        pred = predict(net, d)
        d[ord(c)] = 0
    c = s[-1]
    while 1:
        d[ord(c)] = 1
        pred = predict(net, d)
        d[ord(c)] = 0
        pred = [pred[i] for i in range(256)]
        ind = sample(pred)
        c = chr(ind)
        prob += math.log(pred[ind])
        if len(tac) and tac[-1] == '.':
            break
        tac = tac + c
    return (tac, prob)

def predict_tactics(net, s, n):
    tacs = []
    for i in range(n):
        reset_rnn(net)
        tacs.append(predict_tactic(net, s))
    tacs = sorted(tacs, key=lambda x: -x[1])
    return tacs

#./darknet detect cfg/yolov3.cfg yolov3.weights data/gyoza.jpg

DARKNET_CFG,DARKNET_WEIGHTS=DARKNET_DIR+"cfg/yolov3.cfg", DARKNET_DIR+"yolov3.weights"
print 'cfg',DARKNET_CFG, 'weights',DARKNET_WEIGHTS
net = load_net(DARKNET_CFG, DARKNET_WEIGHTS, 0)
print 'load_net finished'
#t = predict_tactics(net, "+++++\n", 10)
#print t
#print 'load_tactics finished'
meta = load_meta(DARKNET_DIR + "cfg/coco.data")
print 'finish loading meata'
r = detect(net, meta, DARKNET_DIR + "data/eagle.jpg")
print r

