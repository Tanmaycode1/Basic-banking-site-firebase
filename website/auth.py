import os

from flask import Blueprint, render_template, request, flash, redirect, url_for,Response,jsonify
from flask_login import current_user
import mysql.connector
import random
import smtplib
from fpdf import FPDF

auth = Blueprint('auth', __name__)

x=0
y=0
z=0
b=0
p=0
g=0
t=0
uh=0
ev=0
fn=0
p1=00
pn=0
bc=0
rr=0
@auth.route('/', methods=['GET', 'POST'])
def login():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tkgr80786",
        database="project2"
    )
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        global x
        x=email
        print(x)
        con=mydb.cursor()
        sql="""select password from banklogin where email=('%s')""" %email
        con.execute(sql)
        d=con.fetchall()
        pas= 0
        for i in d:
           for m in i:
                pas=m
        if password==pas:
            flash('LOGGED IN SUCCESSFULLY!', category='success')
            return redirect(url_for('auth.home'))
        elif pas==0 :
            flash('USER DOESN\'T EXIST (use a valid email or sign up)',category='error')
        else :
            flash('INCORRECT PASSWORD ,TRY AGAIN',category='error')
    return render_template("login.html", user=current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    email = request.form.get('email')
    first_name = request.form.get('firstname')
    password1 = request.form.get('password1')
    pin= request.form.get('pin')
    balance= request.form.get('balance')
    global bc
    bc=balance
    global pn
    pn=pin
    global p1
    p1=password1
    global ev
    ev=email
    global fn
    fn=first_name

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tkgr80786",
        database="project2"
    )
    con = mydb.cursor()
    sql = """select password from banklogin where email=('%s')""" % email
    con.execute(sql)
    d = con.fetchall()
    p = 0
    global z
    z=first_name
    for i in d:
        for m in i:
            p = m
    con.execute("select email from banklogin where name='%s'"%first_name)
    hjg=con.fetchall()
    oo=0
    for i in hjg:
        for j in i:
            oo=j
    if oo!=0:
        flash('Username already taken ', category='error')
    elif p!=0:
        flash('Email already exists.', category='error')
    elif len(email) < 4:
        flash('Email must be greater than 3 characters.', category='error')
    elif len(first_name) < 2:
        flash('First name must be greater than 1 character.', category='error')
    elif len(password1) < 7:
        flash('Password must be at least 7 characters.', category='error')
    elif len(pin) > 4:
        flash('The pin must be only 4 digits long', category='error')
    elif not pin.isdigit():
        flash('The pin must be only integers', category='error')
    elif not balance.isdigit():
        flash('The balance must be only integers', category='error')
    elif oo==0 :
        # gmail_user = 'gringottsbank3@gmail.com'
        # gmail_password = 'schoolproject'
        # sent_from = gmail_user
        # global rr
        # rr = random.randint(100000, 999999)
        # to = [ev]
        # subject = 'Otp Verfication For Gringotts Bank'
        # body = '''Welcome to Gringgotts Bank Otp For Verfication is "{}"
        # Please don't share this Otp with anyone
        # (We never ask For otp)'''.format(rr)
        # email_text = """\
        # From: %s
        # To: %s
        # Subject: %s
        #
        # %s
        # """ % (sent_from, ", ".join(to), subject, body)
        # smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # smtp_server.ehlo()
        # smtp_server.login(gmail_user, gmail_password)
        # smtp_server.sendmail(sent_from, to, email_text)
        # smtp_server.close()
        global rr
        rr = random.randint(100000, 999999)
        print(rr)
        flash("otp sent",category='success')
        return redirect(url_for('auth.otpverification'))
  return render_template("signup.html", user=current_user)

@auth.route('/home')
def home():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tkgr80786",
        database="project2"
    )
    global x
    email=x
    con = mydb.cursor()
    sql = """select name from banklogin where email=('%s')""" %email
    con.execute(sql)
    d = con.fetchall()
    con.execute("show tables")
    f=con.fetchall()
    pas=0
    for i in d:
        for m in i:
            pas = m
    global y
    y=str(pas).lower()
    ql= "select * from %s"%y
    if (y,) in f:
        con.execute(ql)
        f=con.fetchall()
    else:
       con.execute("CREATE TABLE %s (date datetime,transaction_id int(20),transaction VARCHAR(500) , balance int(100))"%y)
       mydb.commit()
       con.execute("select balance from balance where name='{}'".format(y))

       n=con.fetchall()
       print(n)
       for k in n:
           for kk in k:
               global b
               b=kk
               print(b)
       con.execute("insert into {} values(now(),'111111','Your Account was created !!',{})".format(y,b))
       mydb.commit()
       con.execute(ql)
       f = con.fetchall()
       print(f)
    return render_template("home.html", user=current_user,data=f )

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    global x
    x=0
    global y
    y=0
    global z
    z=0
    return redirect(url_for('auth.login'))
@auth.route('/delhistory')
def delhis():

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tkgr80786",
        database="project2"
    )
    con=mydb.cursor()
    global y
    con.execute("drop table %s"%y)
    mydb.commit()
    con.execute("CREATE TABLE %s (date datetime,transaction_id int(20),transaction VARCHAR(500) , balance int(100))"%y)
    mydb.commit()
    return redirect(url_for('auth.home'))

@auth.route('/delaccount')
def delacc():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tkgr80786",
        database="project2"
    )
    con=mydb.cursor()
    global y
    con.execute("drop table %s"%y)
    mydb.commit()
    global x
    print(x)
    con.execute("delete from banklogin where email='%s'" %x)
    mydb.commit()
    con.execute("delete from balance where name='%s'" %y)
    mydb.commit()
    return redirect(url_for('auth.login'))

@auth.route('/deposit', methods=['GET','POST'])
def addmoney():
  if request.method == 'POST':

    pin = request.form.get('pin')
    amount = request.form.get('amount')

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tkgr80786",
        database="project2"
    )

    con=mydb.cursor()
    global x
    print(x)
    con.execute("select pin from banklogin where email='%s'"%x)

    jj=con.fetchall()
    global p
    pk=random.randint(100000,999999)
    for km in jj:
        for ll in km:
            p=ll

    if not amount.isdigit() :
        flash('The amount must be only integers', category='error')
    elif len(pin) != 4 :
        flash('The pin must be 4 digits long', category='error')
    elif not pin.isdigit():
        flash('The pin must be only integers', category='error')
    elif int(p) !=int(pin):
        flash('Incorect pin', category='error')
    elif int(p)==int(pin):
        print("hi")
        global y
        con.execute("select balance from balance where name='%s'"%y)
        b=con.fetchall()
        t=0
        for i in b:
           for j in i:
               t=j
        nb=int(t)+(int(amount))
        con.execute("update balance set balance={} where name='{}'".format(nb,y))
        mydb.commit()
        con.execute("insert into {} values (now(),{},'You deposited ${}','{}')".format(y,pk,amount,nb))
        mydb.commit()
        return redirect(url_for('auth.home'))
  return render_template("addmoney.html", user=current_user)

@auth.route('/otpverification',methods=['GET','POST'])
def otpverification():
  if request.method == 'POST':
    otp = request.form.get('otp')
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tkgr80786",
        database="project2"
    )
    con=mydb.cursor()
    global rr
    print(rr,otp)
    if not str(otp).isdigit():
        flash("OTP can only be number",category='error')
    elif len(str(otp))>6:
        flash("OTP cannot be longer than 6 digits",category='error')
    elif len(str(otp))<6:
        flash("OTP must be 6 digits long",category='error')
    elif int(otp)==rr:
        global pn
        global fn
        global p1
        global bc
        con.execute(
            "INSERT INTO banklogin(email,name,password,pin) VALUES ('{}','{}','{}','{}');".format(ev, fn,p1,int(pn)))
        con.execute("INSERT INTO balance VALUES ('{}','{}');".format(fn.lower(), int(bc)))
        mydb.commit()
        flash('Account created!', category='success')
        return redirect(url_for('auth.login'))
    elif otp !=  rr:
          flash('Incorrect Otp Please try again', category='error')
  return render_template("otp.html", user=current_user)


@auth.route('/withdraw', methods=['GET','POST'])
def removemoney():
  if request.method == 'POST':

    pin = request.form.get('pin')
    amount = request.form.get('amount')
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tkgr80786",
        database="project2"
    )

    con=mydb.cursor()
    global x
    print(x)
    con.execute("select pin from banklogin where email='%s'"%x)

    jj=con.fetchall()
    global p
    pk=random.randint(100000,999999)
    for km in jj:
        for ll in km:
            p=ll

    if not amount.isdigit() :
        flash('The amount must be only integers', category='error')
    elif len(pin) != 4 :
        flash('The pin must be 4 digits long', category='error')
    elif not pin.isdigit():
        flash('The pin must be only integers', category='error')
    elif int(p) !=int(pin):
        flash('Incorect pin', category='error')
    elif int(p)==int(pin):
        global y
        con.execute("select balance from balance where name='%s'"%y)
        b=con.fetchall()
        t=0
        for i in b:
           for j in i:
               t=j
        nb=int(t)-(int(amount))
        if nb > 0 :
          con.execute("update balance set balance={} where name='{}'".format(nb,y))
          mydb.commit()
          con.execute("insert into {} values (now(),{},'You made a withdrawal of ${}','{}')".format(y,pk,amount,nb))
          mydb.commit()
          return redirect(url_for('auth.home'))
        elif nb==0:
            flash('Your Bank Balance cannot be 0' , category='error')
        else :
            flash('You don\'t have enough balance' , category='error')
  return render_template("withdraw.html", user=current_user)

@auth.route('/sendmoney', methods=['GET','POST'])
def sendmoney():
  if request.method == 'POST':
    r_email = request.form.get('email')
    r_name=request.form.get('name')
    pin = request.form.get('pin')
    amount = request.form.get('amount')
    print(r_name)
    print(r_email)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tkgr80786",
        database="project2"
    )

    con=mydb.cursor()
    global x
    con.execute("select pin from banklogin where email='%s'"%x)
    print(x)
    jj=con.fetchall()
    global p
    for km in jj:
        for ll in km:
            p=ll
    print(p)

    pk=random.randint(100000,999999)
    print(p,pin)
    if not amount.isdigit() :
        flash('The amount must be only integers', category='error')
    elif len(pin) != 4 :
        flash('The pin must be 4 digits long', category='error')
    elif not pin.isdigit():
        flash('The pin must be only integers', category='error')
    elif int(p) !=int(pin):
        flash('Incorect pin', category='error')
    elif int(p)==int(pin):
       print(r_email)
       con.execute("select name from banklogin where email='%s'"%r_email)
       c=con.fetchall()
       print(c)
       global g
       for i in c:
           for j in i:
               g=j
       print(g)
       if len(str(g))<2:
           flash('Reciever email is incorrect ', category='error')
       if len(r_name) < 2 :
        flash('Username cannot be so small ', category='error')
       elif g.lower() !=  r_name.lower() :
        flash('Username doesn\'t match with email entered ', category='error')
       else:
        global y
        con.execute("select balance from balance where name='%s'"%y)
        b=con.fetchall()
        global t
        for i in b:
           for j in i:
               t=j
        kkj=int(t)-(int(amount))
        con.execute("select balance from balance where name='%s'"%r_name)
        pp=con.fetchall()
        global uh
        for i in pp:
           for j in i:
               uh=j
        nb=int(uh)+(int(amount))
        if kkj > 0 :
          con.execute("update balance set balance={} where name='{}'".format(kkj,y))
          mydb.commit()
          con.execute("update balance set balance={} where name='{}'".format(nb,r_name))
          mydb.commit()
          con.execute("insert into {} values (now(),{},'You sent ${} to {}','{}')".format(y,pk,amount,r_name,kkj))
          mydb.commit()
          con.execute("insert into {} values (now(),{},'You recieved ${} from {}','{}')".format(r_name,pk,amount,y,nb))
          mydb.commit()
          return redirect(url_for('auth.home'))
        elif nb==0:
            flash('Your Bank Balance cannot be 0' , category='error')
        else :
            flash('You don\'t have enough balance' , category='error')
  return render_template("sendmoney.html", user=current_user)

@auth.route('/download')
def download_report():
        conn =mysql.connector.connect(
                          host="localhost",
                          user="root",
                          password="tkgr80786",
                          database="project2"
                          )
        cursor = conn.cursor()
        global y
        fs=y
        cc="select * from %s"%fs
        print(cc)
        cursor.execute(cc)
        result = cursor.fetchall()

        pdf = FPDF()
        pdf.add_page()

        page_width = 200

        pdf.set_font('Times', 'B', 30.0)
        pdf.cell(page_width, 0.0, 'PASSBOOK GRINGOTTS BANK', align='C')
        pdf.ln(10)

        pdf.set_font('Courier', '', 12)
        print(page_width)

        pdf.ln(1)

        th = pdf.font_size

        for row in result:
            pdf.cell(52, th, str(row[0]), border=1)
            pdf.cell(18, th, str(row[1]), border=1)
            pdf.cell(100, th, str(row[2]), border=1)
            pdf.cell(25, th, str(row[3]), border=1)
            pdf.ln(th)

        pdf.ln(10)

        pdf.set_font('Times', '', 10.0)
        pdf.cell(page_width, 0.0, '', align='C')

        return Response(pdf.output(dest='S').encode("latin-1"), mimetype='application/pdf',
                        headers={'Content-Disposition': 'attachment;filename=gringotts_bank_passbook.pdf'})
        print(y)
        return redirect(url_for('auth.home'))
@auth.route('/hom')
def hom():
    return render_template("home1.html",user=current_user)

@auth.route('/fp',methods=['GET', 'POST'])
def fp():
    email=request.form.get('email')
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tkgr80786",
        database="project2"
    )
    con = mydb.cursor()
    sql = """select password from banklogin where email=('%s')""" % email
    con.execute(sql)
    d = con.fetchall()
    pas = 0
    for i in d:
        for m in i:
            pas = m
    if pas==0:
            flash('USER DOESN\'T EXIST (use a valid email or sign up)',category='error')
    else:
        gmail_user = 'gringottsbank3@gmail.com'
        gmail_password = 'schoolproject'
        sent_from = gmail_user
        global rr
        rr = random.randint(100000, 999999)
        to = [ev]
        subject = 'Otp Verfication For Gringotts Bank'
        body = '''Welcome to Gringgotts Bank Otp For Verfication is "{}" 
                Please don't share this Otp with anyone
                (We never ask For otp)'''.format(rr)
        email_text = """\
                From: {}
                To: {}
                Subject: {}

                {}
                """ .format(sent_from, ", ".join(to), subject, body)
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        flash("otp sent", category='success')

    return render_template("fp.html",user=current_user)

