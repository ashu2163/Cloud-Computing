from flask import Flask,render_template,request
from datetime import datetime
import sqlite3 as sql
from flask_bootstrap import Bootstrap
import os
import random
import redis
from dbConnection import dbConnect 
from time import time, process_time


r = redis.StrictRedis(host='newapp1.redis.cache.windows.net', port=6380, db=0, password='U0Uh+fEtxuRma2n8BzDarKXqckC3N3KaSLkLKNhtY34=', ssl=True)

# EB looks for an 'application' callable by default.
app = Flask(__name__)

bootstrap = Bootstrap(app)


@app.route('/',methods=['GET','POST'])
def index(): 
    return render_template('index.html')


@app.route("/nstrange", methods=['POST', 'GET'])
def nstrange():
    nst1 = int(request.form['nst1'])
    nst2 = int(request.form['nst2'])
    cursor = dbConnect.cursor()
    #magVal = random.randint(1, 6)
    s=time()
    query = query = "SELECT q.id,l.latitude, l.longitude, l.place, q.mag, q.nst FROM q, l where q.id=l.id and q.nst  >= \'" + str(nst1) + "\' AND q.nst <= \'" + str(nst2) + "\'"
    cursor.execute(query)
    row2 = cursor.fetchall()
    e = time()-s
    #Time = e - s
    #print(Time)
    return render_template('q6.html', time=e, row2=row2)


@app.route("/nstrange1", methods=['POST', 'GET'])
def nstrange1():
    nst1 = int(request.form['nst1'])
    nst2 = int(request.form['nst2'])
    cursor = dbConnect.cursor()
    rannst = random.randint(nst1, nst2)
    s=time()
    query = query = "SELECT q.id,l.latitude, l.longitude, l.place, q.mag, q.nst FROM q, l where q.id=l.id and q.nst  = \'" + str(rannst) + "\'"
    cursor.execute(query)
    row2 = cursor.fetchall()
    e = time()-s
    #Time = e - s
    #print(Time)
    return render_template('q7.html', time=e, row2=row2)


@app.route("/nstrange2", methods=['POST', 'GET'])
def nstrange2():
    nst1 = int(request.form['nst1'])
    nst2 = int(request.form['nst2'])
    num=int(request.form['num'])
    cursor = dbConnect.cursor()
    s=time()
    times=[]
    rows=[]
    for i in range(num):
        s1=time()
        rannst = random.randint(nst1, nst2)
        query = query = "SELECT q.id,l.latitude, l.longitude, l.place, q.mag, q.nst FROM q, l where q.id=l.id and q.nst  = \'" + str(rannst) + "\'"
        cursor.execute(query)
        row2 = cursor.fetchall()
        rows.extend(row2)
        e1=time()-s1
        times.append(e1)
    e = time()-s
    
    return render_template('q8.html', time=e, row2=rows,times=times)


@app.route("/nstrange3", methods=['POST', 'GET'])
def nstrange3():
    nst1 = int(request.form['nst1'])
    nst2 = int(request.form['nst2'])
    num=int(request.form['num'])
    cursor = dbConnect.cursor()
    s = time()
    for i in range(num):
        rannst = random.randint(nst1, nst2)
        query = query = "SELECT q.id,l.latitude, l.longitude, l.place, q.mag, q.nst FROM q, l where q.id=l.id and q.nst  = \'" + str(rannst) + "\'"
        cursor.execute(query)
        row2 = cursor.fetchall()
    e = time()-s

    s1 = time()
    for i in range(num):
        rannst = random.randint(nst1, nst2)
        rkey = 'query1_' + str(rannst)
        if (not r.get(rkey)):
            query = query = "SELECT q.id,l.latitude, l.longitude, l.place, q.mag, q.nst FROM q, l where q.id=l.id and q.nst  = \'" + str(rannst) + "\'"
            cursor.execute(query)
            row1 = cursor.fetchall()
            r.set(rkey, query)
    e1 = time()
    Time1 = e1 - s1
    # print(Time1)
    return render_template('q9.html', time=e, row2=row2, time2=Time1)




@app.route('/Question6')
def Question6():
    return render_template('q6.html')

@app.route('/Question7')
def Question7():
    return render_template('q7.html')

@app.route('/Question8')
def Question8():
    return render_template('q8.html')

@app.route('/Question9')
def Question9():
    return render_template('q9.html')


# port = int(os.getenv('PORT', '3000'))
# app.run(host='0.0.0.0', port=port, debug=True)




