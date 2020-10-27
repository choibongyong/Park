import firebase_admin

from firebase_admin import credentials

from firebase_admin import db

from time import sleep

import cv2

import requests

import json

import os.path

import subprocess

from multiprocessing import Process

from flask import Flask, render_template, Response, url_for

 

cred = credentials.Certificate('fir-project-91285-firebase-adminsdk-i57g9-46d19d060a.json')

firebase_admin.initialize_app(cred,{'databaseURL':'https://fir-project-91285.firebaseio.com/'})

payload= {'apiId': 'phone98150229da9c65996733','apiKey': '5a5146189fa34784a63e4dbf835c3092'}

 

cap = cv2.VideoCapture(0)

#subprocess.check_call("v4l2-ctl -d /dev/video0 -c exposure_auto=1",shell=True)

#subprocess.check_call("v4l2-ctl -d /dev/video0 -c exposure_absolute=0",shell=True)

cap.set(3,340)

cap.set(4,340)

 

img_cnt = 0

file_path = str(img_cnt)+'.jpg'

 

def firedb(frame):

    global img_cnt

    global file_path

 

    check = db.reference('check/isCapture').get()

    if check == 'True':

        cv2.imwrite(file_path, frame)

        img_cnt += 1    

        

        if os.path.isfile(file_path):

            files = [('car_img', open(file_path, 'rb'))]

            res = requests.post('https://api.maum.ai/smartXLoad/PlateRecog', data=payload, files=files).json()

            

            db.reference('check').update({'isCapture':'False'})

                        

            if len(res["plt_num"]) > 5:

                db.reference('plate').update({img_cnt: res['plt_num']})

  

def gen():

    while True:

        ret, frame = cap.read()

 

        if not ret:

            break

        else:

            p1 = Process(target=firedb, args=(frame,))

            p1.start()

           

            ret, jpeg = cv2.imencode('.jpg', frame)

            frame=jpeg.tobytes()

            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

 

app = Flask(__name__)

 

@app.route('/')

def index():

    return render_template('index.html')

	

@app.route('/video_feed')

def video_feed():

    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

 

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080) 
