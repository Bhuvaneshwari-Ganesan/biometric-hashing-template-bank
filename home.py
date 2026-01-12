import os
import shutil
from datetime import date
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.request import urlopen
import smtplib, ssl
import random
import smtplib, ssl
from email import encoders
from urllib import request
from numpy import asarray
import cv2
import imagehash as imagehash
import pymysql
from PIL import Image
from werkzeug.utils import redirect, secure_filename
from test import split_and_store
import ar_master
import camera
import camera1

conn = pymysql.connect(user='root', password='', host='localhost', database='python_biometric_hashing_template_bank',charset='utf8')

from flask import Flask, render_template, flash, request, session, Response, url_for, send_from_directory, current_app, \
    send_file


#from nltk.stem import PorterStemmer

# conn = pymysql.connect(user='root', password='', host='localhost', database='python_biometric_hashing_template')
mm = ar_master.master_flask_code()
# ps = PorterStemmer()
port = 587
smtp_server = "smtp.gmail.com"
sender_email = "serverkey2018@gmail.com"
password ="mlkdrcrjnoimnclw"
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
@app.route("/")
def homepage():
    return render_template('index.html')
@app.route("/admin")
def admin():
    return render_template('admin.html')
@app.route("/admin_login")
def admin1():
    return render_template('admin.html')
#################################################################################################################3
@app.route("/student_deposite")
def student_deposite():
    un=session['uname']
    return render_template('student_deposite.html',vid=un)
@app.route("/amount_deposite",methods = ['GET', 'POST'])
def amount_deposite():
    if request.method == 'POST':
        un = session['bank']
        accno = request.form['accno']
        amount = request.form['amount']
        data = mm.select_direct_query("SELECT status from user_details where account_no='" + accno + "'")
        if data == 'no':
            return 'Username or Password is wrong'
        else:
            old_balance=0
            for row in data:
                old_balance= (row[0])
            new_balance=int(old_balance)+int(amount)
            # print(new_balance)


            mm.insert_query("update user_details set status='"+str(new_balance)+"' WHERE account_no = '"+str(accno)+"'")

            today = date.today()
            cdate = today.strftime("%d-%m-%Y")
            mm.insert_query("insert into user_mini values('"+accno + "','"+amount+"','Deposite','"+cdate+"','0','"+un+"')")

            return render_template('student_deposite.html',msg="Deposite Success",vid=accno)
#####################################################################################################################3
#################################################################################################################3
@app.route("/student_withdraw")
def student_withdraw():
    un=session['uname']

    return render_template('student_withdraw.html',vid=un)
@app.route("/amount_withdraw",methods = ['GET', 'POST'])
def amount_withdraw():
    if request.method == 'POST':
        accno = request.form['accno']
        amount = request.form['amount']
        un = session['bank']
        data=mm.select_direct_query("SELECT status from user_details where account_no='" + accno + "'")
        if data == "no":
            return 'Username or Password is wrong'
        else:
            old_balance=0
            for row in data:
                old_balance= (row[0])
            new_balance=int(old_balance)-int(amount)
            # print(new_balance)
            a=int(old_balance)
            b=int(amount)
            if a<b:
                return render_template('student_withdraw.html',msg="Low Balance",vid=accno)
            else:

                # mm.insert_query('update user_details set status=%s WHERE account_no = %s', (str(new_balance), accno))
                mm.insert_query("update user_details set status='" + str(new_balance) + "' WHERE account_no = '" + str(accno) + "'")

                today = date.today()
                cdate = today.strftime("%d-%m-%Y")
                mm.insert_query("insert into user_mini values('"+accno + "','"+amount+"','Withdraw','"+cdate+"','0','"+un+"')")

                return render_template('student_withdraw.html',msg="Withdraw Success",vid=accno)
##############################################################################################################################
@app.route("/student_ministatement")
def student_ministatement():
    un=session['uname']
    bank=session['bank']
    data=mm.select_direct_query("SELECT account,amount,process,cdate,status,report FROM user_mini where account='"+un+"' and  report='"+bank+"'")
    data1=mm.select_direct_query("SELECT status FROM user_details where account_no='"+un+"' and report='"+bank+"'")

    return render_template('student_ministatement.html',items=data,Bal=data1,vid=un)
#################################################################################################################3
@app.route("/student_transaction")
def student_transaction():
    un=session['uname']
    return render_template('student_transaction.html',vid=un)
def transaction_to(a,b,fraccout):
    un=session['uname']

    cursor = conn.cursor()
    cursor.execute("SELECT status,report from user_details where account_no='" + a + "'")
    data = cursor.fetchall()
    if data is None:
        return render_template('student_transaction.html',msg="Account Not Found",vid=un)
    else:
        old_balance=0
        receiver_bank=''
        # print(data)
        for row in data:
             old_balance= (row[0])
             receiver_bank= (row[1])
        new_balance=int(old_balance)+int(b)
        conn1 = pymysql.connect(user='root', password='', host='localhost', database='python_biometric_hashing_template_bank',charset='utf8')
        cursor = conn.cursor()
        cursor.execute('update user_details set status=%s WHERE account_no = %s', (str(new_balance), a))
        conn.commit()
        cursor1 = conn1.cursor()
        today = date.today()
        cdate = today.strftime("%d-%m-%Y")
        cursor1.execute("insert into user_mini values('"+a + "','"+b+"','Ceredit','"+cdate+"','"+fraccout+"','"+receiver_bank+"')")
        conn1.commit()
        conn1.close()

@app.route("/amount_transaction",methods = ['GET', 'POST'])
def amount_transaction():
    sender_bank = session['bank']
    if request.method == 'POST':
        accno = request.form['accno']
        amount = request.form['amount']
        toaccount = request.form['toaccount']
        cursor = conn.cursor()

        cursor.execute("SELECT status from user_details where account_no='" + accno + "'")
        data = cursor.fetchone()
        # print(data)
        if data is None:
            return 'Failed'
        else:
            old_balance=0

            for row in data:
                old_balance= (row)

            new_balance=int(old_balance)-int(amount)
            # print(new_balance)
            a=int(old_balance)
            b=int(amount)
            if a<b:
                return render_template('student_transaction.html',msg="Low Balance",vid=accno)
            else:
                transaction_to(toaccount,amount,accno)
                conn1 = pymysql.connect(user='root', password='', host='localhost', database='python_biometric_hashing_template_bank',charset='utf8')
                cursor = conn.cursor()
                cursor.execute('update user_details set status=%s WHERE account_no = %s', (str(new_balance), accno))
                conn.commit()

                cursor1 = conn1.cursor()
                today = date.today()
                cdate = today.strftime("%d-%m-%Y")
                cursor1.execute("insert into user_mini values('"+accno + "','"+amount+"','Debit','"+cdate+"','"+toaccount+"','"+sender_bank+"')")
                conn1.commit()
                conn1.close()
                return render_template('student_transaction.html',msg="Transaction Success",vid=accno)
##############################################################################################################################
@app.route("/admin_login", methods = ['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':
            return render_template('admin_home.html',error=error)
        else:
            return render_template('admin.html', error=error)
@app.route("/admin_home")
def adminhome():
    return render_template('admin_home.html')
@app.route("/admin_student")
def adminstudent():
    data=mm.select_direct_query("select bank_name from bank_details")
    maxin = mm.select_direct_query("select * from user_details")
    maxin=len(maxin)
    if maxin==0:
        maxin=1
    else:
        maxin=maxin+1
    maxin=100+int(maxin)
    return render_template('admin_student.html',bank=data,maxin=maxin)

@app.route("/add_student",methods = ['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        bank = request.form['select']
        roolno = request.form['roolno']
        studentname = request.form['studentname']
        class1 = request.form['class1']
        section = request.form['section']
        fathername = request.form['fathername']
        contact = request.form['contact']
        email = request.form['email']
        address = request.form['address']

        # maxin=mm.find_max_id("user_details")
        conn = pymysql.connect(user='root', password='', host='localhost', database='python_biometric_hashing_template_bank',charset='utf8')
        session['roolno'] = section
        cursor = conn.cursor()
        cursor.execute("insert into user_details values('"+roolno + "','"+studentname+"','"+class1+"','"+section+"','"+fathername+"','"+contact+"','"+email+"','"+address+"','0','"+bank+"','-','-')")
        conn.commit()
        conn.close()
        #flash("Logged in successfully.")
        #return 'file uploaded successfully'
        return render_template('admin_student1.html',vid=section)
@app.route('/video_feed')
def video_feed():
    return Response(gen(camera.VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



@app.route('/video_feed1')
def video_feed1():
    return Response(gen(camera1.VideoCamera1()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/add_face',methods=['POST','GET'])
def view_voter():
    if request.method=='POST':
        vid=request.form['vid']
        fimg=vid+".jpg"
        conn = pymysql.connect(user='root', password='', host='localhost', database='python_biometric_hashing_template_bank',charset='utf8')
        cursor = conn.cursor()
        cursor.execute('update user_details set report=%s WHERE name = %s', (fimg, vid))
        conn.commit()
        conn.close()
        shutil.copy('faces/f1.jpg', 'static/photo/face/'+fimg)
        img = cv2.imread('faces/f1.jpg', 0)
        numpydata = asarray(img)
        rr=0
        for x in numpydata:
            for y in x:
                rr=rr+int(y)
        # print(rr)

        dd = split_and_store()
        k=dd.generte_key(6)
        k1=dd.generte_key(6)
        plain_text=str(rr)
        chyper_text = dd.encrypt(plain_text)
        session['face']=chyper_text
        return render_template('admin_student2.html',vid=vid)


@app.route('/add_iris', methods=['POST', 'GET'])
def view_voter1():
    if request.method == 'POST':
        vid = request.form['vid']
        fimg = vid + ".jpg"

        shutil.copy('faces/f1.jpg', 'static/photo/iris/' + fimg)
        img = cv2.imread('faces/f1.jpg', 0)
        numpydata = asarray(img)
        rr = 0
        for x in numpydata:
            for y in x:
                rr = rr + int(y)
        dd = split_and_store()
        k = dd.generte_key(6)
        k1 = dd.generte_key(6)
        plain_text = str(rr)
        iris = dd.encrypt(plain_text)
        face=session['face']
        en_date=iris+","+face
        dd.split_file(en_date,vid)
        mm.insert_query("update user_details set public_key='"+str(k)+"',private_key='"+str(k1)+"' where account_no='"+str(vid)+"'")
        return render_template('student.html')


@app.route("/admin_upload")
def admin_upload():
    return render_template('admin_upload.html')

@app.route('/upload_data',methods=['POST','GET'])
def upload_data():
    mycursor = conn.cursor()
    if request.method=='POST':
        name = request.form['class1']
        caption = request.form['subject']
        if 'file' not in request.files:
            flash('No file Part')
            return redirect(request.url)
        file= request.files['file']
        # print(file)
        f = request.files['file']
        f.save(os.path.join("static/uploads/", secure_filename(f.filename)))
        cursor = conn.cursor()
        today = date.today()
        rdate = today.strftime("%d-%m-%Y")
        cursor.execute("SELECT max(id)+1 FROM   question")
        maxid = cursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO question  VALUES (%s, %s, %s, %s, %s)"
        val = (maxid, name, caption, f.filename,  rdate)
        # print(val)
        cursor.execute(sql,val)
        conn.commit()
    return render_template('admin_home.html')

@app.route("/bank_register",methods = ['GET', 'POST'])
def bank_register():
    if request.method == 'POST':
        bank_name = request.form['bank_name']
        incharge = request.form['incharge']
        branch = request.form['branch']
        address = request.form['address']
        contact = request.form['contact']
        email = request.form['email']
        password = request.form['password']

        conn = pymysql.connect(user='root', password='', host='localhost', database='python_biometric_hashing_template_bank',charset='utf8')
        cursor = conn.cursor()
        cursor.execute("insert into bank_details values('"+bank_name + "','"+incharge+"','"+branch+"','"+address+"','"+contact+"','"+email+"','"+password+"','0','0')")
        conn.commit()
        conn.close()
        return render_template('bank_register.html',data='success')
    return render_template('bank_register.html')



@app.route("/bank",methods = ['GET', 'POST'])
def bank():
    if request.method == 'POST':
        n = request.form['uname']
        g = request.form['cont']
        branch = request.form['branch']
        cursor = conn.cursor()
        session['bank'] = n
        qq="SELECT * from bank_details where bank_name='" + str(n) + "'and branch='"+str(branch)+"' and password='"+str(g)+"'"
        # print(qq)
        cursor.execute(qq)
        data = cursor.fetchall()
        data1=len(data)
        # print(data)
        if data1 <=0:
            return 'Username or Password is wrong'
        else:
            session['bank'] = request.form['uname']
            session['branch'] = request.form['branch']
            session['password'] = request.form['cont']
            return redirect(url_for('bank_home', vid=n))
            # return render_template('bank_home.html',vid=n)
    return render_template('bank.html')

@app.route("/bank_home")
def bank_home():
    bank=session['bank']
    branch=session['branch']
    data=mm.select_direct_query("select * from bank_details where bank_name='"+str(bank)+"' and branch='"+str(branch)+"'")
    return render_template('bank_home.html',vid=bank,items=data)


@app.route("/bank_home1",methods = ['GET', 'POST'])
def bank_home1():
    bank=session['bank']
    data=mm.select_direct_query("select * from bank_details where bank_name='"+str(bank)+"'")
    return render_template('bank_home1.html',vid=bank,items=data)


@app.route("/bank_home2",methods = ['GET', 'POST'])
def bank_home2():
    un=session['bank']
    branch=session['branch']
    if request.method == 'POST':

        incharge = request.form['studentname']
        contact = request.form['email']
        email = request.form['address']
        password = request.form['address2']


        conn = pymysql.connect(user='root', password='', host='localhost', database='python_biometric_hashing_template_bank',charset='utf8')
        cursor = conn.cursor()
        cursor.execute("update bank_details set incharge='"+str(incharge)+"',contact='"+str(contact)+"',email='"+str(email)+"',password='"+str(password)+"' where bank_name='"+str(un)+"' and branch='"+str(branch)+"'")
        conn.commit()
        conn.close()
        return redirect(url_for('bank_home', msg='success'))
    return render_template('bank_home1.html')



@app.route("/bank_transaction")
def bank_transaction():
    un=session['bank']
    ddd = mm.select_direct_query("select account,amount,process,cdate,status from user_mini where report='" + str(un) + "'")
    return render_template('bank_transaction.html',vid=un,items=ddd)


@app.route("/bank_user")
def bank_user():
    un=session['bank']
    branch=session['branch']
    ddd = mm.select_direct_query("select account_no,name,contact,email,branch,address,dob from user_details where report='" + str(un) + "' and branch='"+str(branch)+"'")
    return render_template('bank_user.html',vid=un,items=ddd)

@app.route("/student")
def student():
    return render_template('student.html')


@app.route("/student_login",methods = ['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        n = request.form['uname']
        g = request.form['cont']
        cursor = conn.cursor()
        session['roolno'] = n
        qq="SELECT * from user_details where account_no='" + str(n) + "' and password='"+str(g)+"'"
        # print(qq)
        cursor.execute(qq)
        data = cursor.fetchall()
        data1=len(data)
        # print(data)
        if data1 <=0:
            return 'Username or Password is wrong'
        else:
            for x in data:
                name=x[0]
                contact=x[1]
                email=x[2]
                account_no=x[3]
                branch=x[4]
                address=x[5]
                bank=x[9]
                session['name'] = name
                session['contact'] =contact
                session['email'] =email
                session['account_no'] = account_no
                session['branch'] = branch
                session['address'] =address
                session['bank'] = bank
            session['uname'] = request.form['uname']

            return render_template('student_face_verification.html',sid=n)
@app.route('/verify_face',methods=['POST','GET'])
def verify_face():
    msg=""
    sid=request.form['uname']
    # print(sid)
    if request.method=='POST':
        if 1==1:
            shutil.copy('faces/f1.jpg', 'faces/s1.jpg')
            hash0 = imagehash.average_hash(Image.open("faces/s1.jpg"))
            hash1 = imagehash.average_hash(Image.open("static/photo/face/"+sid+".jpg"))
            cc1=hash0 - hash1
            # print(cc1)
            img = cv2.imread('faces/f1.jpg', 0)
            numpydata = asarray(img)
            rr = 0
            for x in numpydata:
                for y in x:
                    rr = rr + int(y)
            session['face_value']=str(rr)
            session['face_value1']=str(cc1)
            session['vid']=str(sid)
            today = date.today()
            return redirect(url_for('verify_iris', msg=msg))
            # if cc1<=10:
            #
            #     return redirect(url_for('student_home', msg=msg))
            # else:
            #     return redirect(url_for('student', msg=msg))

    return render_template('verify_face.html',msg=msg)


@app.route('/verify_iris',methods=['POST','GET'])
def verify_iris():
    msg=""
    sid=session['vid']
    # print(sid)
    if request.method=='POST':
        if 1==1:
            shutil.copy('faces/f1.jpg', 'faces/s1.jpg')
            hash0 = imagehash.average_hash(Image.open("faces/s1.jpg"))
            hash1 = imagehash.average_hash(Image.open("static/photo/iris/"+sid+".jpg"))
            cc1=hash0 - hash1
            # print(cc1)
            img = cv2.imread('faces/f1.jpg', 0)
            numpydata = asarray(img)
            rr = 0
            for x in numpydata:
                for y in x:
                    rr = rr + int(y)
            session['iris_value']=str(rr)
            session['iris_value1']=str(cc1)
            session['vid']=str(sid)
            today = date.today()
            return redirect(url_for('user_otp', msg=msg))



    return render_template('student_iris_verification.html',msg=msg)


@app.route("/user_otp")
def user_otp():
    vid=session['vid']
    ddd=mm.select_direct_query("select email,private_key,report from user_details where account_no='"+str(vid)+"'")
    email=(ddd[0][0])
    msg = MIMEMultipart()
    fromaddr = "serverkey2018@gmail.com"
    msg['From'] = fromaddr
    msg['To'] = email
    msg['Subject'] = "Private Key"
    body = ""+str(ddd[0][1])
    msg.attach(MIMEText(body, 'plain'))
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, email, text)
    s.quit()
    session['otp']=ddd[0][1]
    session['bank']=ddd[0][2]
    return render_template('user_otp1.html')


@app.route("/user_otp1",methods=['POST','GET'])
def user_otp1():
    if request.method=='POST':
        otp1 = request.form['uname']
        otp=session['otp']
        # print(otp,otp1)
        if otp == otp1:
            vid=session['vid']
            session['uname']=vid
            face_value = session['face_value']
            iris_value=session['iris_value']
            x1 = os.path.join("data/", vid + ".txt")
            cypher_text=''

            with open(x1) as f1:
                cypher_text = f1.readlines()

            ddd=cypher_text[0].split(",")
            key1,key2=ddd[0],ddd[1]
            # print(key1,key2)
            dd = split_and_store()
            face_train=dd.decrypt(key1)
            iris_train=dd.decrypt(key2)

            face_verification=((int(face_train)/int(face_value))*1)
            iris_verification=((int(iris_train)/int(iris_value))*1)
            # print(face_train,face_value)
            # print(iris_train,iris_value)
            # print(face_verification,iris_verification)
            if face_verification > 0.8 and iris_verification >0.8:
                un = session['uname']
                # return render_template('student_home.html',vid=un)
                return student_home()
            elif(face_verification<0.8):
                return render_template('student.html',data='Face Not Matched')
            elif (iris_verification < 0.8):
                return render_template('student.html', data='Iris Not Matched')
            else:
                return render_template('user_otp1.html', data='')
        else:
            return render_template('user_otp1.html', data='OTP Not Matched')


    else:
        return render_template('user_otp.html')



@app.route("/student_home")
def student_home():
    un=session['uname']
    data=mm.select_direct_query("select * from user_details where account_no='"+str(un)+"'")
    return render_template('student_home.html',vid=un,items=data)



@app.route("/student_home1",methods = ['GET', 'POST'])
def student_home1():
    un=session['uname']
    data=mm.select_direct_query("select * from user_details where account_no='"+str(un)+"'")
    return render_template('student_home1.html',vid=un,items=data)



@app.route("/student_home2",methods = ['GET', 'POST'])
def student_home2():
    un=session['uname']
    if request.method == 'POST':
        name = request.form['roolno']
        contact = request.form['studentname']
        email = request.form['class1']
        address = request.form['contact']
        dob = request.form['email']
        password = request.form['address']

        conn = pymysql.connect(user='root', password='', host='localhost', database='python_biometric_hashing_template_bank',charset='utf8')
        cursor = conn.cursor()
        cursor.execute("update user_details set name='"+str(name)+"',contact='"+str(contact)+"',email='"+str(email)+"',address='"+str(address)+"',dob='"+str(dob)+"',password='"+str(password)+"' where account_no='"+str(un)+"'")
        conn.commit()
        conn.close()
        return redirect(url_for('student_home', msg='success'))
    return render_template('student_home1.html')



@app.route("/student_question")
def student_question():
    return render_template('student_question.html')

@app.route("/search_question1",methods=['POST','GET'])
def search_question1():
    if request.method=='POST':
        name = request.form['textfield']
        name1 = request.form['textfield2']
        cur = conn.cursor()
        #cur.execute("SELECT * FROM question where class1='"+name+"' and subject='"+name1+"'")
        cur.execute("SELECT * FROM question where class1='"+name+"' and subject='"+name1+"'")
        data = cur.fetchall()
        # print(data)
        return render_template('search_question_1.html', data=data)
    else:
        return student_question()

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # print(filename)
    uploads = os.path.join(current_app.root_path, "static/uploads/")
    # print(uploads)
    f=filename
    return send_from_directory(directory=uploads, filename=filename,as_attachment=True)

@app.route("/student_attendance", methods=['GET', 'POST'])
def student_attendance():
    n= session['roolno']
    # print(n)
    cur = conn.cursor()
    cur.execute ("SELECT id,sid,rdate,month FROM attendance where sid='"+n+"'")
    return render_template('student_attendance.html',items=cur.fetchall())


@app.route("/admin_attendance")
def admin_attendance():
    cur = conn.cursor()
    cur.execute ("SELECT id,sid,rdate,month FROM attendance")
    return render_template('admin_attendance.html',items=cur.fetchall())

    #return render_template('history.html')


@app.route("/admin_user")
def admin_user():
    cur = conn.cursor()
    cur.execute ("SELECT name,contact,email,account_no,branch,address,dob,report FROM user_details")
    return render_template('admin_user.html',items=cur.fetchall())



@app.route("/admin_bank")
def admin_bank():
    cur = conn.cursor()
    cur.execute ("SELECT bank_name,incharge,branch,address,contact,email  FROM bank_details")
    return render_template('admin_bank.html',items=cur.fetchall())

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
