
import sys, os
#sys.path.append(os.path.join(os.getcwd(),'python/'))

import darknet as dn
import pdb
from flask import Flask

"""
r = dn.detect(net, meta, "data/bedroom.jpg")
print r
# And then down here you could detect a lot more images like:
r = dn.detect(net, meta, "data/eagle.jpg")
print r
r = dn.detect(net, meta, "data/giraffe.jpg")
print r
r = dn.detect(net, meta, "data/horses.jpg")
print r
"""

app=Flask(__name__)

@app.route("/")
def index():
    return "hello world"

@app.route("/detect")
def detect():
    r = dn.detect(net, meta, "data/person.jpg")
#    print r
    return "detect"+r

if __name__ == '_main__':
    dn.set_gpu(0)
    net = dn.load_net("cfg/yolo-thor.cfg", "/home/pjreddie/backup/yolo-thor_final.weights", 0)
    meta = dn.load_meta("cfg/thor.data")
    app.run(host="0.0.0.0",port=3000)
