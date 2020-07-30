import os
import shutil
import csv
import sys
import sqlite3 as sql
from datetime import datetime

from flask import Flask, render_template, url_for, flash, redirect, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_bootstrap import Bootstrap
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired
import ibm_db

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/magnituderange1', methods=['GET', 'POST'])
def magnituderange1():
    fromM = int(request.form['mag1'])
    toM = int(request.form['mag2'])
    div = int(request.form['div1'])
    connection = sql.connect("quakes.db")
    cursor = connection.cursor()
    d = (float(toM) - float(fromM)) / float(div)
    row=[]
    print(d)
    while int(div) > 0:
        query = "select id, place, latitude, longitude, mag from quakes1 where mag > \'" + str(fromM) + "\' and mag < \'" + str(float(fromM)+float(d)) + "\' order by mag "
        cursor.execute(query)
        col = cursor.fetchall()
        row.append(col)
        
        fromM += d
        div -= 1
    #print(row[1])
    cursor.close()
    return render_template('newmag.html', col=row,div=d)

@app.route('/tworange', methods=['GET', 'POST'])
def tworange():
    lat = request.form['latitude1']
    long0 = request.form['longitude1']
    lat1 = request.form['latitude2']
    long1 = request.form['longitude2']


    connection = sql.connect("quakes.db")
    cursor = connection.cursor()
    query = "SELECT id, latitude, longitude, time, place FROM quakes1 where latitude >= \'" + str(lat) + "\' AND latitude <= \'" + str(lat1) + "\' AND longitude >= \'" + str(long0) + "\'AND longitude <= \'" + str(long1) + "\'"
    cursor.execute(query)
    #connection.commit()
    out = cursor.fetchall()
    cursor.close()
    return render_template('tworange.html', out=out)


@app.route('/locrecent', methods=['GET', 'POST'])
def locrecent():
    loc = request.form['loc']
    connection = sql.connect("quakes.db")
    cursor = connection.cursor()
    query = "SELECT longitude, latitude, mag, time from quakes1 where place LIKE '%"+ str(loc) +"%' and mag < 4"
    print(query)
    cursor.execute(query)
    col = cursor.fetchall()
    row = []
    count = 0
    for c in col:
        timex = c[3].split("T")[0]
        if(timex <= '2020-06-17' and timex >= '2020-06-13'):
            count += 1
            row.append(c)
    cursor.close()
    return render_template('sal.html', col=row, loc=loc)


@app.route('/largest1', methods=['GET', 'POST'])
def largest1():

    connection = sql.connect("quakes.db")
    cursor = connection.cursor()
    query = "SELECT locationSource, id, mag from quakes1 order by mag desc limit 1"
    cursor.execute(query)
    col = cursor.fetchall()
    cursor.close()
    cursor1 = connection.cursor()
    query1 = "select count(*) from quakes"
    cursor1.execute(query1)
    col1 = cursor1.fetchall()
    cursor1.close()
    return render_template('largest.html', col=col, col1=col1)


@app.route('/largedallas', methods=['GET', 'POST'])
def largedallas():
    radius = request.form['radius']
    lat = request.form['latitude']
    long1 = request.form['longitude']
    north = float(lat) + float(radius) / 111
    south = float(lat) - float(radius) / 111
    east = float(long1) + float(radius) / 111
    west = float(long1) - float(radius) / 111
    connection = sql.connect("quakes.db")
    cursor = connection.cursor()
    query = "SELECT latitude, longitude, mag FROM quakes1 where latitude >= \'" + str(south) + "\' AND latitude <= \'" + str(north) + "\' AND longitude >= \'" + str(west) + "\'AND longitude <= \'" + str(east) + "\' order by mag desc limit 1"
    cursor.execute(query)
    col = cursor.fetchall()
    cursor.close()
    return render_template('largest.html', col=col)


@app.route('/magni', methods=['GET', 'POST'])
def magni():
    st = request.form['start']
    end = request.form['end']
    connection = sql.connect("quakes.db")
    cursor = connection.cursor()
    query = "SELECT mag, time from quakes1 where mag >= \'" + str(st) + "\' AND mag <= \'" + str(end) + "\'"
    cursor.execute(query)
    col = cursor.fetchall()
    row = []
    count = 0
    startdate = datetime.strptime('2020-06-10', '%Y-%m-%d')
    for c in col:
        timex = c[1].split("T")[0]
        print(st)
        if (datetime.strptime(timex, '%Y-%m-%d') > startdate):
            count += 1
            row.append(c)
            print(end)
    cursor.close()
    return render_template('quakes.html', col=row, count = count)


@app.route('/range', methods=['GET', 'POST'])
def range():
    radius = request.form['radius']
    lat = request.form['latitude']
    long1 = request.form['longitude']
    north = float(lat) + float(radius) / 111
    south = float(lat) - float(radius) / 111
    east = float(long1) + float(radius) / 111
    west = float(long1) - float(radius) / 111
    
    connection = sql.connect("quakes.db")
    cursor = connection.cursor()
    query = "SELECT latitude, longitude, mag FROM quakes1 where latitude >= \'" + str(south) + "\' AND latitude <= \'" + str(north) + "\' AND longitude >= \'" + str(west) + "\'AND longitude <= \'" + str(east) + "\'"
    query1 = "SELECT COUNT(latitude) FROM quakes1 where latitude >= \'" + str(south) + "\' AND latitude <= \'" + str(north) + "\' AND longitude >= \'" + str(west) + "\'AND longitude <= \'" + str(east) + "\'"
    cursor.execute(query1)
    out = cursor.fetchall()
    cursor.execute(query)
    out1 = cursor.fetchall()

    return render_template('range.html', out=out, out1=out1)




@app.route('/daterange', methods=['GET', 'POST'])
def daterange():
    mindate = request.form['mindate']
    maxdate = request.form['maxdate']
    connection = sql.connect("quakes.db")
    cursor = connection.cursor()
    query = "SELECT longitude, latitude, mag, time from quakes1 where mag > 3 "
    cursor.execute(query)
    col = cursor.fetchall()
    row = []
    count = 0
    for c in col:
        timex = c[3].split("T")[0]
        if(timex >= mindate and timex <= maxdate):
            count += 1
            row.append(c)
    cursor.close()
    print(row.__len__())
    return render_template('daterange.html', col=row, count = count)


@app.route('/getRange', methods=['GET', 'POST'])
def getRange():
    fr = request.form['nm']
    to = request.form['cpt']
    connection = sql.connect("quakes.db")
    cursor = connection.cursor()
    query = "UPDATE quakes1 SET Caption = \'" + to + "\' where Name = \'" + fr + "\'"
    cursor.execute(query)
    connection.commit()
    query1 = "Select name, picture, caption from quakes1 where name = \'" + fr + "\'"
    cursor1 = connection.cursor()
    cursor1.execute(query1)
    entry = cursor1.fetchall()
    cursor.close()
    cursor1.close()
    return render_template('test.html', entry=entry)


@app.route('/Question6')
def Question6():
    return render_template('newmag.html')

@app.route('/Question7')
def Question7():
    return render_template('tworange.html')

@app.route('/Question8')
def Question8():
    return render_template('sal.html')

@app.route('/Question9')
def Question9():
    return render_template('largest.html')


port = int(os.getenv('PORT', '3000'))
app.run(host='0.0.0.0', port=port,debug=True)
