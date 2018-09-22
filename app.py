
import sys, os
#sys.path.append(os.path.join(os.getcwd(),'python/'))
from pydarknet import Detector,Image
from icecream import ic

import pdb
from flask import Flask,flash,redirect

app=Flask(__name__)

@app.route("/")
def index():
    return "hello world"

@app.route("/test")
def test():
    img=Image(cv2.imread("data/person.jpg"))
    ret=net.detect(img)
    ic(ret)
    return str(ret)


@app.route("/detect",methods=['GET','POST'])
def detect():
    if request.method=="POST":
        file=request.files['file']
        if file.filename == '':
            flash('no file is uploaded')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename=secure_filename(file.filename)
            file.save(os,path.join(app.config["UPLOAD_FOLDER"],filename))
            return redirect(url_for('uploaded_file',filename=filename))
    elif request.method=="GET":
        return """
        <!doctype html>
        <h1>upload file</h1>
        <form method=post enctype="multipart/form-data">
            <input type=file name=file>
            <input type=submit value=upload>
        </form>
        """

if __name__ == '__main__':
    cfg,weights,data="cfg/yolov3.cfg", "python/conf/yolov3.weights","cfg/coco.data"
    net = Detector(bytes(cfg,encoding="utf-8"),bytes(weights,encoding="utf-8"),0,bytes(data,encoding="utf-8"))
    app.run(host="0.0.0.0",port=3000)
