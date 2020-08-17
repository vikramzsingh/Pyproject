#Project for semester 6th

import time
import os

from flask import Flask,render_template,request,url_for,session,redirect,send_file
import pymysql # not used as conectivity is done in mylib python file
from werkzeug.utils import secure_filename

from mylib import*

app=Flask(__name__) #create app(Application name)
app.secret_key="super secret key"
app.config['UPLOAD_FOLDER']='./static/photos'

@app.route('/') #home page
def index():
    if ("usertype" in session):
        usertype = session["usertype"]
        userid = session["userid"]  # Not used
        if (usertype == "student"):
            return redirect(url_for('studenthome'))
        elif (usertype == "admin"):
            return redirect(url_for('adminhome'))
    else:
        cur=connect_to_database()
        sql="select * from solutiondata order by s_id desc"
        cur.execute(sql)
        n=cur.rowcount
        if(n>=1):
            data=cur.fetchall()
            return render_template('QueAndSol.html',data=data)
        else:
            return render_template('index.html')


@app.route('/about') #home page
def about():
    return render_template('AboutTemp.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/slashboard/')
def slashboard():
    try:
        return render_template('ThisDoesDotExist.html')
    except Exception as e:
        return render_template('500.html', error=e)
"""
@app.route('/return_file') #home page
def return_files():
    return send_file('./static/test.pdf',attachment_filename='test.pdf')


@app.route('/file_download') #home page
def file_download():
    return render_template('Downloads.html')
"""
#For Student
@app.route('/studentreg',methods=['GET','POST'])
def studentreg():
    if(request.method=='POST'):
        try:
            name=request.form["T1"]
            rollno=request.form["T2"]
            branch=request.form["T3"]
            year=request.form["T4"]
            address=request.form["T5"]
            mobileno=request.form["T6"]
            email=request.form["T7"]
            password=request.form["T8"]
            usertype="student"
            branch=branch.upper()
            cur=connect_to_database() # connectivity to database

            # for studentdata table
            sql1="insert into studentdata values('"+name+"','"+rollno+"','"+branch+"','"+year+"','"+address+"','"+mobileno+"','"+email+"')"
            cur.execute(sql1) # executing Query
            n=cur.rowcount # No. of rows executed

            # for logindata table
            sql2="insert into logindata values('"+email+"','"+password+"','"+usertype+"')"
            cur.execute(sql2)  # executing Query
            m=cur.rowcount  # No. of rows executed

            msg="Error!! Cannot save data try again."
            if(n==1 and m==1):
                msg="Student data saved and login created successfully"
            elif(n==1):
                msg="Student data saved but login not created"
            elif(m==1):
                msg="Student data not saved but login created successfully"

            return render_template('Studentreg.html', msg=msg)
        except:
            return render_template('StudentRegError.html')

    else:
        return render_template('Studentreg.html')




#For Admin
@app.route('/adminreg',methods=['GET','POST'])
def adminreg():
    if (request.method == 'POST'):
        try:
            name=request.form["T1"]
            depmt=request.form["T2"]
            address=request.form["T3"]
            mobileno = request.form["T4"]
            email=request.form["T5"]
            password=request.form["T6"]
            usertype="admin"
            cur=connect_to_database()  # connectivity to database

            # for admindata table
            sql1="insert into admindata values('"+name+"','"+depmt+"','"+address+"','"+mobileno+"','"+email+"')"
            cur.execute(sql1)  # executing Query
            n=cur.rowcount  # No. of rows executed

            # for logindata table
            sql2="insert into logindata values('" +email+ "','" +password+"','"+usertype+"')"
            cur.execute(sql2)  # executing Query
            m=cur.rowcount  # No. of rows executed

            msg="Error!! Cannot save data try again."
            if(n==1 and m==1):
                msg="Admin data saved and login created successfully"
            elif(n==1):
                msg="Admin data saved but login not created"
            elif(m==1):
                msg="Admin data not saved but login created successfully"

            return render_template('Adminreg.html', msg=msg)
        except:
            return render_template('AdminRegError.html')

    else:
        return render_template('AdminReg.html')

# For Login
@app.route('/login',methods=['GET','POST'])
def login():
    if(request.method=='POST'):
        userid=request.form["T1"]
        password=request.form["T2"]
        #connectivity to databse and creation of cursor
        cur=connect_to_database()
        #valid sql statement
        sql="select * from logindata where userid='"+userid+"' AND password='"+password+"'"
        #execute statement
        cur.execute(sql)
        #response
        n=cur.rowcount

        if(n>0):
            data=cur.fetchone()
            usertype=data[2]
            session["userid"]=userid
            session["usertype"]=usertype
            if(usertype=="student"):
                return redirect(url_for('studenthome'))
            elif(usertype=="admin"):
                return redirect(url_for('adminhome'))
            else:
                return render_template('Login.html',msg="Contact to Admin")
        else:
            return render_template('Login.html',msg="Invalid User ID and Password")
    else:
        return render_template('Login.html')


# For Logout
@app.route('/logout')
def logout():
    if("usertype" in session):
        session.pop("usertype",None)
        session.pop("userid",None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


# for AuthError(Authentication Error)
@app.route('/autherror')
def autherror():
    return render_template('AuthError.html')


#studenthome redirection
@app.route('/studenthome',methods=['GET','POST'])
def studenthome():
    if("usertype" in session):
        usertype=session["usertype"]
        userid=session["userid"] # Not used
        if(usertype=="student"):
            return render_template('StudentHome.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('login'))


#For Profile in StudentHome
@app.route('/studentprofile',methods=['GET','POST'])
def studentprofile():
    if("usertype" in session):
        userid=session["userid"]
        usertype=session["usertype"]
        if(usertype=="student"):

            # connectivity to database
            cur=connect_to_database()

            # valid sql statement
            sql="select * from studentdata where email='"+userid+"'"

            #excute sql stmt
            cur.execute(sql)

            #response
            n=cur.rowcount

            if(n==1):
                data=cur.fetchone()
                photo=check_photo(userid)
                return render_template('StudentProfile.html',data=data,photo=photo)
            else:
                return render_template('StudentProfile.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('login'))



@app.route('/editstudent', methods=['GET', 'POST'])
def editstudent():
    if ("usertype" in session):
        userid = session["userid"]
        usertype = session["usertype"]
        if (usertype == "student"):
            if request.method == 'POST':
                email=request.form["H1"]

                cur=connect_to_database()

                sql="select *from studentdata where email='"+email+"'"

                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template('EditStudent.html',res=data)
                else:
                    return render_template('EditStudent.html',msg="Not data found")
            else:
                return redirect(url_for('studentprofile'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


#to save data in form
@app.route('/editstudent1',methods=['GET','POST'])
def editstudent1():
    if ("usertype" in session):
        userid = session["userid"]
        usertype = session["usertype"]
        if (usertype == "student"):
            if request.method=='POST':
                name=request.form["T1"]
                year=request.form["T4"]
                address=request.form["T5"]
                mobileno=request.form["T6"]
                email=request.form["T7"]
                cur = connect_to_database()

                sql="update studentdata set name='"+name+"', year='"+year+"', address='"+address+"',mobileno='"+mobileno+"' where email='"+email+"'"

                cur.execute(sql)
                n=cur.rowcount

                if(n>0):
                    return redirect(url_for('studentprofile'))
                else:
                    return redirect(url_for('studentprofile'))
            else:
                return redirect(url_for('studentprofile'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))



@app.route('/uploadstudentphoto',methods=['GET','POST'])
def uploadstudentphoto():
    if("usertype" in session):
        userid=session["userid"]
        usertype=session["usertype"]
        if(usertype=="student"):
            if(request.method=='POST'):
                file=request.files["F1"]
                if file:
                    path = os.path.basename(file.filename)
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time())) + '.' + file_ext
                    filename = secure_filename(filename)
                    cur = connect_to_database()
                    sql = "insert into photodata values('" + userid + "','" + filename + "')"
                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if (n == 1):
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            return redirect(url_for('studentprofile'))
                        else:
                            return render_template('UploadStudentPhoto.html',msg="Failed")
                    except:
                        return render_template('UploadStudentPhoto.html',msg="Duplicate(as insert show duplicate but update querry not")
                else:
                    return redirect(url_for('StudentProfile'))
            else:
                return redirect(url_for('autherror'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))



@app.route('/uploadquestionstudent',methods=['GET','POST'])
def uploadquestionstudent():
    if ("usertype" in session):
        userid = session["userid"]
        usertype = session["usertype"]
        if (usertype == "student"):
            return render_template('UploadQuestionStudent.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/uploadquestionstudent1',methods=['GET','POST'])
def uploadquestionstudent1():
    if("usertype" in session):
        userid=session["userid"]
        usertype=session["usertype"]
        if(usertype=="student"):
            if(request.method=='POST'):
                que=request.form["T1"]
                sub=request.form["T2"]
                qdate=int(time.time())

                cur=connect_to_database()
                sql="select * from studentdata where email='"+userid+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    name=data[0]
                    rollno=data[1]

                #valid sql statement
                    sql1="insert into questiondata(question,subject,question_date,name,roll_no,email) values('"+que+"','"+sub+"',"+str(qdate)+",'"+name+"','"+rollno+"','"+userid+"')"
                    cur.execute(sql1)
                    m=cur.rowcount
                if(n==1 and m==1):
                    return render_template('QuestionUploaded.html')
                else:
                    return render_template('UploadQuestionStudent.html')
            else:
                return redirect(url_for('autherror'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/uploadsolution',methods=['GET','POST'])
def uploadsolution():
    if("usertype" in session):
        userid=session["userid"]
        usertype=session["usertype"]
        if(usertype=="student"):
            cur=connect_to_database()
            #valid sql statement
            sql="select * from questiondata where email<>'"+userid+"' order by question_date desc" # Means lattest entry display first
            cur.execute(sql)
            n=cur.rowcount
            if(n>=1):
                data1=cur.fetchall()
                return render_template('SolveQuestions.html',data=data1)
            else:
                return render_template('SolveQuestions.html',msg="No msg available")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/uploadsolution1',methods=['GET','POST'])
def uploadsolution1():
    if ("usertype" in session):
        userid=session["userid"]
        usertype=session["usertype"]
        if (usertype=="student"):
            if(request.method=='POST'):
                qid=request.form["T1"]
                return render_template('UploadSolution.html',qid=qid)
            else:
                redirect(url_for('autherror'))
        else:
            redirect(url_for('autherror'))
    else:
        redirect(url_for('autherror'))


@app.route('/uploadsolution2',methods=['GET','POST'])
def uploadsolution2():
    if ("usertype" in session):
        userid=session["userid"]
        usertype=session["usertype"]
        if (usertype=="student"):
            if(request.method=='POST'):
                solution = request.form["T1"]
                qid=request.form["T2"]
                cur=connect_to_database()
                sql1= "select * from questiondata where q_id='"+qid+"'"
                cur.execute(sql1)
                m=cur.rowcount
                if(m==1):
                    data1=cur.fetchone()
                    question=data1[1]

                sql="select * from studentdata where email='"+userid+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    name=data[0]
                    sql1="insert into solutiondata(q_id,solution,name,question) values('"+qid+"','"+solution+"','"+name+"','"+question+"')"
                    cur.execute(sql1)
                    m=cur.rowcount
                    if(n==1 and m==1):
                       return render_template('SolutionUploaded.html')
                    else:
                        return redirect(url_for('uploadsolution'))
                else:
                    return redirect(url_for('uploadsolution'))
            else:
                return redirect(url_for('uploadsolution'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/payfees',methods=['GET','POST'])
def payfees():
    if("usertype" in session):
        userid=session["userid"]
        usertype=session["usertype"]
        if(usertype=="student"):
            return render_template('PayFeesForm.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))



@app.route('/payfees1',methods=['GET','POST'])
def payfees1():
    if("usertype" in session):
        userid=session["userid"]
        usertype=session["usertype"]
        if(usertype=="student"):
            try:
                if(request.method=='POST'):
                    name=request.form["T1"]
                    roll_no=request.form["T2"]
                    branch=request.form["T3"]
                    mobile_no=request.form["T4"]
                    amount=request.form["T5"]
                    acc_no=request.form["T6"]
                    transfer_to=request.form["T7"]

                    # connectivity
                    cur=connect_to_database()

                    #valid sql
                    sql="insert into feesdata values('"+name+"','"+roll_no+"','"+branch+"','"+mobile_no+"','"+userid+"','"+amount+"','"+acc_no+"','"+transfer_to+"')"

                    #execute sql
                    cur.execute(sql)

                    #check response
                    n=cur.rowcount

                    if(n==1):
                        sql1="select * from feesdata where email='"+userid+"'"
                        cur.execute(sql1)
                        m=cur.rowcount
                        if(n==1 and m==1):
                            data=cur.fetchone()
                            return render_template('PaymentDetail.html',data=data)
                        else:
                            return render_template('PaymentDetail.html',msg="Payment Error!! Fees not paid")
                    else:
                        return redirect(url_for('autherror'))
                else:
                    return redirect(url_for('autherror'))
            except:
                sql1="select * from feesdata where email='" + userid + "'"
                cur.execute(sql1)
                m=cur.rowcount
                if (m == 1):
                    data = cur.fetchone()
                    return render_template('PaymentDetail.html', data=data,msg="You have already paid your fees")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/student_change_password',methods=['GET','POST'])
def student_change_password():
    if("usertype" in session):
        userid=session["userid"]
        usertype=session["usertype"]
        if(usertype=="student"):
            if request.method=='POST':
                oldpass=request.form["T1"]
                newpass=request.form["T2"]

                #connectivity
                """con = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="b316", autocommit=True)
                cur = con.cursor()"""

                #connectivity
                cur=connect_to_database()

                #valid sql statement
                sql="update logindata set password='"+newpass+"' where password='"+oldpass+"' AND userid='"+userid+"'"
                print(sql)
                cur.execute(sql)
                n=cur.rowcount
                if(n>0):
                    return render_template('StudentPasswordChange.html',msg="Password changed")
                else:
                    return render_template('StudentPasswordChange.html',msg="Invalid old password")
            else:
                return render_template('StudentPasswordChange.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))





#------------------------------------------------------------------------------------------------------------------#

#adminhome redirection
@app.route('/adminhome',methods=['GET','POST'])
def adminhome():
    if("usertype" in session):
        usertype=session["usertype"]
        userid=session["userid"] # Not used
        if(usertype=="admin"):
            return render_template('AdminHome.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


#For Profile in AdminHome
@app.route('/adminprofile',methods=['GET','POST'])
def adminprofile():
    if("usertype" in session):
        userid=session["userid"] # email recieved as user id of admin
        usertype=session["usertype"]
        if(usertype=="admin"):

            # connectivity to database
            cur=connect_to_database()

            # valid sql statement
            sql="select * from admindata where email='"+userid+"'"

            #excute sql stmt
            cur.execute(sql)

            #response
            n=cur.rowcount

            if(n==1):
                data=cur.fetchone()
                return render_template('AdminProfile.html',data=data)
            else:
                return render_template('AdminProfile.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/student_record',methods=['GET','POST'])
def student_record():
    if("usertype" in session):
        userid=session["userid"]
        usertype=session["usertype"]
        if(usertype=="admin"):
            # connectivity
            cur=connect_to_database()

            #valid sql
            sql="select * from feesdata"

            #execute stmt
            cur.execute(sql)

            #response
            n=cur.rowcount
            if(n>0):
                data=cur.fetchall()
                return render_template('StudentRecord.html',data=data)
            else:
                return redirect(url_for('StudentRecord.html',msg="No data found"))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/student_data',methods=['GET','POST'])
def student_data():
    return render_template('StudentData.html')

@app.route('/student_data1',methods=['GET','POST'])
def student_data1():
    if ("usertype" in session):
        userid = session["userid"]
        usertype = session["usertype"]
        if (usertype == "admin"):
            # connectivity
            branch="CSE"
            # branch=brach.Upper() .Upper() to convert cse into upper case
            cur = connect_to_database()

            # valid sql
            sql = "select * from studentdata where branch='"+branch+"'"

            # execute stmt
            cur.execute(sql)

            # response
            n = cur.rowcount
            if (n > 0):
                data=cur.fetchall()
                return render_template('StudentData1.html',data=data)
            else:
                return render_template('StudentData1.html',msg="No data found")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/student_data2',methods=['GET','POST'])
def student_data2():
    if ("usertype" in session):
        userid = session["userid"]
        usertype = session["usertype"]
        if (usertype == "admin"):
            # connectivity
            branch="IT"
            cur = connect_to_database()

            # valid sql
            sql = "select * from studentdata where branch='"+branch+"'"

            # execute stmt
            cur.execute(sql)

            # response
            n = cur.rowcount
            if (n > 0):
                data=cur.fetchall()
                return render_template('StudentData1.html',data=data)
            else:
                return render_template('StudentData1.html',msg="No data found")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/student_data3',methods=['GET','POST'])
def student_data3():
    if ("usertype" in session):
        userid = session["userid"]
        usertype = session["usertype"]
        if (usertype == "admin"):
            # connectivity
            branch="MECHANICAL"
            cur = connect_to_database()

            # valid sql
            sql = "select * from studentdata where branch='"+branch+"'"

            # execute stmt
            cur.execute(sql)

            # response
            n = cur.rowcount
            if (n > 0):
                data=cur.fetchall()
                return render_template('StudentData1.html',data=data)
            else:
                return render_template('StudentData1.html',msg="No data found")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/student_data4',methods=['GET','POST'])
def student_data4():
    if ("usertype" in session):
        userid = session["userid"]
        usertype = session["usertype"]
        if (usertype == "admin"):
            # connectivity
            branch="CIVIL"
            cur = connect_to_database()

            # valid sql
            sql = "select * from studentdata where branch='"+branch+"'"

            # execute stmt
            cur.execute(sql)

            # response
            n = cur.rowcount
            if (n > 0):
                data=cur.fetchall()
                return render_template('StudentData1.html',data=data)
            else:
                return render_template('StudentData1.html',msg="No data found")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/student_data5',methods=['GET','POST'])
def student_data5():
    if ("usertype" in session):
        userid = session["userid"]
        usertype = session["usertype"]
        if (usertype == "admin"):
            # connectivity
            branch="BioTech"
            cur = connect_to_database()

            # valid sql
            sql = "select * from studentdata where branch='"+branch+"'"

            # execute stmt
            cur.execute(sql)

            # response
            n = cur.rowcount
            if (n > 0):
                data=cur.fetchall()
                return render_template('StudentData1.html',data=data)
            else:
                return render_template('StudentData1.html',msg="No data found")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))



@app.route('/admin_change_password',methods=['GET','POST'])
def admin_change_password():
    if("usertype" in session):
        userid=session["userid"]
        usertype=session["usertype"]
        if(usertype=="admin"):
            if request.method=='POST':
                oldpass=request.form["T1"]
                newpass=request.form["T2"]

                #connectivity
                """con = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="b316", autocommit=True)
                cur = con.cursor()"""

                #connectivity
                cur=connect_to_database()

                #valid sql statement
                sql="update logindata set password='"+newpass+"' where password='"+oldpass+"' AND userid='"+userid+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n>0):
                    return render_template('AdminChangePassword.html',msg="Password changed")
                else:
                    return render_template('AdminChangePassword.html',msg="Invalid old password")
            else:
                return render_template('AdminChangePassword.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))



if __name__=='__main__':
    app.run(debug=True)