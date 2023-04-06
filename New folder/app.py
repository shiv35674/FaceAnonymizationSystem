from logging import info
import cv2
from flask import Flask, request, render_template
from tqdm.gui import trange, tqdm


app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/', methods=['POST','GET'])
def show():
    name2=request.form['vid']


    face_cascade = cv2.CascadeClassifier("C:\\Python36-64\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(name2)
    img_array = []
    

    f=0
    for f in trange(500, desc="Processing", bar_format="{desc}: {percentage:3.0f}%"):
        _, img = cap.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        for (x, y, w, h) in faces:
            ROI = img[y:y + h, x:x + w]
            blur = cv2.GaussianBlur(ROI, (27, 27), 0)
            img[y:y + h, x:x + w] = blur

            height, width, layers = img.shape
            size = (width, height)

        img_array.append(img)

    cap.release()
    out = cv2.VideoWriter('video_processed.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

    return render_template('index.html',info="Anonymized video successfully saved in the folder containing the original video.")

if __name__ == '__main__':
    app.run(debug=True)