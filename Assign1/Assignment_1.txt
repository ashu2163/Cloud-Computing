from flask import Flask,render_template,request
from datetime import datetime
import sqlite3 as sql
from flask_bootstrap import Bootstrap
import os

# EB looks for an 'application' callable by default.
application = Flask(__name__)
bootstrap = Bootstrap(application)


@application.route('/',methods=['GET','POST'])
def index(): 
    return render_template('index.html')

# @application.route('/demo',methods=['GET','POST'])
# def demo():
#     name=request.form['n1']
#     return render_template('index.html',name=name)

@application.route('/searchImg',methods=['GET','POST'])
def searchImg():
    name=request.form['name']
    connection=sql.connect("sql.db")
    cursor=connection.cursor()
    q1="Select Picture from data where Name = '"+str(name) + "'"
    cursor.execute(q1)
    col=cursor.fetchall()
    return render_template('SearchImg.html',col=col,name=name)


# @application.route('/search',methods=['GET','POST'])
# def searchId():
#     num=request.form['id']
#     connection=sql.connect("sql.db")
#     cursor=connection.cursor()
#     q1="Select Picture, Caption from names where ID = '"+str(num) + "'"
#     cursor.execute(q1)
#     col=cursor.fetchall()
    
#     return render_template('searchID.html',a=col)

# @application.route('/update',methods=['GET','POST'])
# def update():
#     name=request.form['n1']
#     comment=request.form['comment']
#     connection=sql.connect("sql.db")
#     cursor=connection.cursor()
#     q1="Update names set Caption='"+str(comment)+"' where Name = '"+str(name) +"'"
#     c=cursor.execute(q1)
#     #rowupdate=c.rowcount
#     connection.commit()
#     cursor.close()
#     cursor1=connection.cursor()
#     q2="Select Name,Picture,Caption from names where Name = '"+str(name)+"'"
#     cursor1.execute(q2)
#     col=cursor1.fetchall()
#     return render_template('Update.html',col=col)


@application.route('/searchbySalary',methods=['GET','POST'])
def searchbySalary():
    num=int(request.form['num1'])
    connection=sql.connect("sql.db")
    cursor=connection.cursor()
    q1="Select Name,Salary,Picture from data where Salary < "+str(num)
    cursor.execute(q1)
    col=cursor.fetchall()
    
    return render_template('searchbySalary.html',col=col)

@application.route('/updatePicture',methods=['GET','POST'])
def updatePicture():
    name=request.form['name']
    picture=request.form['picname']
    if name=="" or picture=="":
        return "No string entered"
    connection=sql.connect("sql.db")
    cursor=connection.cursor()
    q1="Update data set Picture='"+str(picture)+"' where Name='"+str(name) +"'"
    c=cursor.execute(q1)
    connection.commit()
    cursor.close()
    cursor1=connection.cursor()
    q2="Select Name,Picture from data where Name= '"+ str(name) +"'"
    cursor1.execute(q2)
    col=cursor1.fetchall()
    return render_template('updatePicture.html',col=col)

@application.route('/deleteEntry',methods=['GET','POST'])
def deleteEntry():
    connection=sql.connect("sql.db")
    
    name=request.form['name1']
    #connection=sql.connect("sql.db")
    cursor=connection.cursor()
    query="Delete from data where Name= '"+str(name) + "'"
    
    c=cursor.execute(query)
    connection.commit()
    rowdeleted= c.rowcount
    print(rowdeleted)
    cursor.close()

    cursor1=connection.cursor()
    q1="Select Name from data"
    cursor1.execute(q1)
    names=cursor1.fetchall()
    cursor1.close()
    return render_template('deleteEntry.html',rowdeleted=rowdeleted,names=names)
        

# @application.route('/getpic', methods=['GET', 'POST'])
# def getpic():
#     picname = request.form['picname']
#     connection = sql.connect("sql.db")
#     cursor = connection.cursor()
#     q1 = "SELECT Picture from data where Picture = '"+str(picname)+"'" 
#     cursor.execute(q1)
#     e = cursor.fetchall()
#     return render_template('index.html', entry=e, name=picname)




@application.route('/Question6')
def Question6():
    return render_template('SearchImg.html')

@application.route('/Question7')
def Question7():
    return render_template('searchbySalary.html')

@application.route('/Question8')
def Question8():
    return render_template('updatePicture.html')

@application.route('/Question9')
def Question9():
    connection=sql.connect("sql.db")
    cursor1=connection.cursor()
    q1="Select Name from data"
    cursor1.execute(q1)
    names=cursor1.fetchall()
    return render_template('deleteEntry.html',names=names)


# @app.route('/Question7')
# def Question7():
#     return render_template('UpdateGrades.html')



# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    # application.debug = True
    # application.run()
    port = int(os.getenv('PORT', '3000'))
    application.run(host='0.0.0.0', port=port,debug=True)