import os

# -------------------- ENV CHECK --------------------
IS_RENDER = os.environ.get("RENDER") == "true"

# -------------------- IMPORTS --------------------
import shutil
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from numpy import asarray
import cv2
import imagehash
import pymysql
from PIL import Image
from werkzeug.utils import redirect, secure_filename

from flask import (
    Flask, render_template, flash, request, session,
    Response, url_for, send_from_directory, current_app
)

import ar_master
import camera
import camera1
from test import split_and_store

# -------------------- DATABASE --------------------
conn = None
if not IS_RENDER:
    conn = pymysql.connect(
        user='root',
        password='',
        host='localhost',
        database='python_biometric_hashing_template_bank',
        charset='utf8'
    )

# -------------------- APP CONFIG --------------------
app = Flask(__name__)
app.secret_key = '7d441f27d441f27567d441f2b6176a'

mm = ar_master.master_flask_code()

# -------------------- EMAIL CONFIG --------------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "serverkey2018@gmail.com"
EMAIL_PASSWORD = "mlkdrcrjnoimnclw"

# -------------------- BASIC PAGES --------------------
@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/student")
def student():
    return render_template("student.html")

# -------------------- RENDER SAFE BLOCK --------------------
def render_disabled():
    return "This feature is disabled in live demo (Render)."

# -------------------- CAMERA ROUTES --------------------
@app.route('/video_feed')
def video_feed():
    if IS_RENDER:
        return render_disabled()

    return Response(gen(camera.VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed1')
def video_feed1():
    if IS_RENDER:
        return render_disabled()

    return Response(gen(camera1.VideoCamera1()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(cam):
    while True:
        frame = cam.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# -------------------- STUDENT LOGIN --------------------
@app.route("/student_login", methods=["POST"])
def student_login():
    if IS_RENDER:
        return render_disabled()

    acc = request.form['uname']
    pwd = request.form['cont']

    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM user_details WHERE account_no=%s AND password=%s",
        (acc, pwd)
    )
    data = cursor.fetchall()

    if not data:
        return "Invalid login"

    session['uname'] = acc
    return render_template("student_face_verification.html", sid=acc)

# -------------------- FACE VERIFY --------------------
@app.route("/verify_face", methods=["POST"])
def verify_face():
    if IS_RENDER:
        return render_disabled()

    sid = request.form['uname']
    shutil.copy('faces/f1.jpg', 'faces/s1.jpg')

    h1 = imagehash.average_hash(Image.open("faces/s1.jpg"))
    h2 = imagehash.average_hash(Image.open(f"static/photo/face/{sid}.jpg"))

    if (h1 - h2) > 10:
        return "Face not matched"

    return redirect(url_for("verify_iris"))

# -------------------- IRIS VERIFY --------------------
@app.route("/verify_iris")
def verify_iris():
    if IS_RENDER:
        return render_disabled()

    return render_template("student_iris_verification.html")

# -------------------- OTP --------------------
@app.route("/user_otp")
def user_otp():
    if IS_RENDER:
        return render_disabled()

    vid = session['uname']
    cursor = conn.cursor()
    cursor.execute(
        "SELECT email, private_key FROM user_details WHERE account_no=%s",
        (vid,)
    )
    email, otp = cursor.fetchone()

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    msg['Subject'] = "Your OTP"
    msg.attach(MIMEText(otp, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, EMAIL_PASSWORD)
    server.sendmail(SENDER_EMAIL, email, msg.as_string())
    server.quit()

    session['otp'] = otp
    return render_template("user_otp1.html")

# -------------------- HOME --------------------
@app.route("/student_home")
def student_home():
    if IS_RENDER:
        return render_template("student_home.html", demo=True)

    acc = session['uname']
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_details WHERE account_no=%s", (acc,))
    data = cursor.fetchall()
    return render_template("student_home.html", items=data)

# -------------------- FILE DOWNLOAD --------------------
@app.route('/uploads/<path:filename>')
def download(filename):
    uploads = os.path.join(current_app.root_path, "static/uploads")
    return send_from_directory(uploads, filename, as_attachment=True)

# -------------------- MAIN --------------------
if __name__ == "__main__":
    app.run()
