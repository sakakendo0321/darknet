
import sys, os
import cv2
#sys.path.append(os.path.join(os.getcwd(),'python/'))
from pydarknet import Detector,Image
from icecream import ic

import pdb
from flask import Flask,flash,redirect,request,url_for
from werkzeug.utils import secure_filename

app=Flask(__name__)
app.config['UPLOAD_FOLDER']="./static/uploads"
result=""

def allowed_file(filename):
    ALLOWED_EXTENSIONS=set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return """
    <!doctype html>
    <a href=/detect>detect</a>
    <a href=/result>result</a>
    """

@app.route("/test")
def test():
    img=Image(cv2.imread("data/person.jpg"))
    ret=net.detect(img)
    ic(ret)
    return str(ret)

def getDetect(filename):
    ic(filename)
    return net.detect(Image(cv2.imread(filename)))

@app.route("/detect",methods=['GET','POST'])
def detect():
    if request.method=="POST":
        file=request.files['file']
        if file.filename == '':
            flash('no file is uploaded')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
            result=getDetect(app.config["UPLOAD_FOLDER"]+"/"+filename)
#            result=net.detect(Image(cv2.imread(app.config["UPLOAD_FOLDER"]+filename)))
            ic(result)
            return str(result)
#            return redirect(url_for('index',filename=filename))
    elif request.method=="GET":
        return """
        <!doctype html>
        <h1>upload file</h1>
        <form method=post enctype="multipart/form-data">
            <input type=file name=file>
            <input type=submit value=upload>
        </form>
        """
@app.route("/uploaded_file")
def uploaded_file():
    return """
    <!doctype html>
    <h1>uploaded file</h1>
    """

@app.route("/result")
def result():
    return """
    """

if __name__ == '__main__':
    cfg,weights,data="cfg/yolov3.cfg", "./yolov3.weights","cfg/coco.data"
    net = Detector(bytes(cfg,encoding="utf-8"),bytes(weights,encoding="utf-8"),0,bytes(data,encoding="utf-8"))
    app.run(host="0.0.0.0",port=5000)
