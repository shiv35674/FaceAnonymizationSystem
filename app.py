from logging import info
import cv2
from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from tqdm.gui import trange
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Shivam/Desktop/software/software/database.db'
db = SQLAlchemy(app)



class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

@app.route('/home')
def hello_world():
    return render_template('index.html')

@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/home', methods=['POST','GET'])
def show():
    name2=request.form['vid']
    
    # face_cascade = cv2.CascadeClassifier("C:\\Python36-64\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml")
    face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(name2)
    img_array = []
    f=0
    
    for j in trange(500,desc="Processing",bar_format="{desc}: {percentage:3.0f}%"):
        _, img = cap.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        for (x, y, w, h) in faces:
            ROI = img[y:y+h, x:x+w]
            blur = cv2.GaussianBlur(ROI, (27,27), 0)
            img[y:y+h, x:x+w] = blur
            
            height, width, layers = img.shape
            size = (width,height)

        
        img_array.append(img)
                
    cap.release()
    out = cv2.VideoWriter('video_processed.mp4',cv2.VideoWriter_fourcc(*'DIVX'),15,size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

    return render_template('index.html',info="Anonymized Video successfully exported to original path")

# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         uname = request.form['unames']
#         mail = request.form['mail']
#         passw = request.form['passwo']

#         register = user(username = uname, email = mail, password = passw)
#         db.session.add(register)
#         db.session.commit()
#         return redirect(url_for("login"))
#     return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['unames']
        mail = request.form['mail']
        passw = request.form['passwo']
        flag=0;
        SpecialSym =['$', '@', '#', '%']
        # Check that the password is at least 8 characters long
        if len(passw) < 8:
            flag=1;
            return redirect(request.url)

        # Check that the password contains at least one uppercase letter, one lowercase letter, and one number
        if not any(char.isupper() for char in passw):
            flag=1;
            return redirect(request.url)
        if not any(char.islower() for char in passw):
            flag=1;
            return redirect(request.url)
        if not any(char.isdigit() for char in passw):
            flag=1;
            return redirect(request.url)
        if not any(char in SpecialSym for char in passw):
            flag=1;
            return redirect(request.url)
        # Add the user to the database
        if flag==0:
            register = user(username = uname, email = mail, password = passw)
            db.session.add(register)
            db.session.commit()
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        
        login = user.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return redirect(url_for('show'))
    return render_template("login.html")

if __name__=='__main__':
    
    app.run(debug=True)
    