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

@app.route('/selectv', methods=['GET', 'POST'])
def selectv():
    idd= request.form['id']
    connect = sql.connect("quakes.db")
    cursor = connection.cursor()
    query = "select * from q join l where l.id = \'" + str(idd) + "\' and q.id=l.id "
    cursor.execute(query)
    col = cursor.fetchall()
    mag=col[0][3]
    magfro=mag-0.1
    magto=mag+0.1
    query1 = "select * from q join l where q.id=l.id and q.mag >= '"+ str(magfrom) +"' and q.mag <= '"+ str(magto) +"'"
    cursor.execute(query1)
    col1 = cursor.fetchall()
    print(len(col1[0]))
    col1.extend(col)
    return render_template('selectv.html', col=col1)



# @app.route('/magnituderange1', methods=['GET', 'POST'])
# def magnituderange1():
#     fromM = int(request.form['mag1'])
#     toM = int(request.form['mag2'])
#     div = int(request.form['div1'])
#     connection = sql.connect("quakes.db")
#     cursor = connection.cursor()
#     d = (float(toM) - float(fromM)) / float(div)
#     row=[]
#     while int(div) > 0:
#         query = "select id, place, latitude, longitude, mag from quakes1 where mag >= \'" + str(fromM) + "\' and mag < \'" + str(float(fromM)+float(d)) + "\' order by mag "
#         cursor.execute(query)
#         col = cursor.fetchall()
#         row.append(col)
        
#         fromM += d
#         div -= 1
#     #print(row[1])
#     cursor.close()
#     return render_template('newmag.html', col=row,div=d)

@app.route('/tworange', methods=['GET', 'POST'])
def tworange():
    lat = request.form['latitude1']
    long0 = request.form['longitude1']
    lat1 = request.form['latitude2']
    long1 = request.form['longitude2']
    fromdepth=request.form['fdepth']
    todepth=request.form['tdepth']

    connection = sql.connect("quakes.db")
    cursor = connection.cursor()
    if lat>lat1:
        temp=lat1
        lat1=lat
        lat=temp
    if long0 > long1:
        temp=long1
        long1=long0
        long0=temp
    query = "SELECT q.id,l.latitude, l.longitude, q.depth, l.place, q.time, q.mag FROM q join l where q.id=l.id and l.latitude  >= \'" + str(lat) + "\' AND l.latitude <= \'" + str(lat1) + "\' AND l.longitude >= \'" + str(long0) + "\'AND l.longitude <= \'" + str(long1) + "\' and q.depth >= '"+ str(fromdepth)+"' and q.depth <= '"+ str(todepth) +"' order by q.mag desc LIMIT 3 "
    cursor.execute(query)
    #connection.commit()
    out = cursor.fetchall()
    cursor.close()
    return render_template('tworange.html', out=out)


@app.route('/locrecent', methods=['GET', 'POST'])
def locrecent():
    loc = request.form['loc']
    fromdepth=request.form['fdepth']
    todepth=request.form['tdepth']
    dist=request.form['dist']
    connection = sql.connect("quakes.db")
    cursor = connection.cursor()
    query = "SELECT longitude, latitude from l where place LIKE '%"+ str(loc) +"%'"
    cursor.execute(query)
    col = cursor.fetchall()
    north = float(col[0][1]) + float(dist) / 111
    south = float(col[0][1]) - float(dist) / 111
    east = float(col[0][0]) + float(dist) / 111
    west = float(col[0][0]) - float(dist) / 111
    query1 = "SELECT l.latitude, l.longitude, q.mag, l.place, q.depth, q.time FROM q join l where q.id=l.id and l.latitude >= \'" + str(south) + "\' AND l.latitude <= \'" + str(north) + "\' AND l.longitude >= \'" + str(west) + "\'AND l.longitude <= \'" + str(east) + "\' and q.depth >= '"+ str(fromdepth) +"' and q.depth <= '"+ str(todepth) +"' order by mag desc limit 1"
    cursor.execute(query1)
    col = cursor.fetchall()
    cursor.close()
    return render_template('sal.html', col=col)


@app.route('/latlon', methods=['GET', 'POST'])
def latlon():
    lat = request.form['latitude1']
    long0 = request.form['longitude1']
    lat1 = request.form['latitude2']
    long1 = request.form['longitude2']
    nlarge=request.form['n']
    connection = sql.connect("quakes.db")
    cursor = connection.cursor()
    if lat>lat1:
        temp=lat1
        lat1=lat
        lat=temp
    if long0 > long1:
        temp=long1
        long1=long0
        long0=temp
    query = "SELECT q.id,l.latitude, l.longitude, q.depth, l.place, q.time, q.mag FROM q join l where q.id=l.id and l.latitude  >= \'" + str(lat) + "\' AND l.latitude <= \'" + str(lat1) + "\' AND l.longitude >= \'" + str(long0) + "\'AND l.longitude <= \'" + str(long1) + "\' order by q.mag desc LIMIT '"+ str(nlarge) +"'"
    cursor.execute(query)
    col = cursor.fetchall()
    cursor.close()
    return render_template('q8a.html', col=col)

@app.route('/q8a', methods=['GET', 'POST'])
def q8a():
    idd=request.form['id']
    time=request.form['time']
    lat=request.form['latitude']
    lon=request.form['longitude']
    place=request.form['place']
    connection = sql.connect("quakes.db")
    cursor = connection.cursor()
    query="Update q set time= '"+ str(time) +"' where q.id= '"+ str(idd) +"'"
    q1="Update l set latitude= '"+ str(lat) +"', longitude= '"+ str(lon) +"', place= '"+ str(place) +"'  where id= '"+ str(idd) +"'"
    col=cursor.execute(query).rowcount
    col1=cursor.execute(q1).rowcount
    connection.commit()
    cursor.close()
    if col:
        return render_template('q8a.html', col1=col)
    else:
        return render_template('q8a.html', entry="Entry not found..")


@app.route('/latplace', methods=['GET', 'POST'])
def latplace():
    place1= request.form['place1']
    place2= request.form['place2']
    connection = sql.connect("quakes.db")
    cursor = connection.cursor()
    col1=[]
    col2=[]
    if place1 != '' and place2 != '':
        query1= "Select latitude, longitude from l where place = '"+ str(place1) +"'"
        query2= "Select latitude, longitude from l where place = '"+ str(place2) +"'"
        cursor.execute(query1)
        col1 = cursor.fetchall()
        cursor.execute(query2)
        col2 = cursor.fetchall()
    if len(col1) != 0:
        lat=col1[0]
        long0=col1[1]
    else:
        lat = request.form['latitude1']
        long0 = request.form['longitude1']
    if len(col2) != 0:
        lat1=col2[0]
        long2=col2[1]
    else:    
        lat1 = request.form['latitude2']
        long1 = request.form['longitude2']
    
    if lat>lat1:
        temp=lat1
        lat1=lat
        lat=temp
    if long0 > long1:
        temp=long1
        long1=long0
        long0=temp
    
    mag1=request.form['mag1']
    mag2=request.form['mag2']
    
    query = "SELECT q.id,l.latitude, l.longitude, q.depth, l.place, q.time, q.mag FROM q join l where q.id=l.id and l.latitude  >= \'" + str(lat) + "\' AND l.latitude <= \'" + str(lat1) + "\' AND l.longitude >= \'" + str(long0) + "\'AND l.longitude <= \'" + str(long1) + "\' AND q.mag >= \'" + str(mag1) + "\' AND q.mag <= \'" + str(mag2) + "\' order by q.mag desc "
    
    cursor.execute(query)
    col = cursor.fetchall()
    cursor.close()
    return render_template('q9.html', col=col)


# @app.route('/largest1', methods=['GET', 'POST'])
# def largest1():

#     connection = sql.connect("quakes.db")
#     cursor = connection.cursor()
#     query = "SELECT locationSource, id, mag from quakes1 order by mag desc limit 1"
#     cursor.execute(query)
#     col = cursor.fetchall()
#     cursor.close()
#     cursor1 = connection.cursor()
#     query1 = "select count(*) from quakes"
#     cursor1.execute(query1)
#     col1 = cursor1.fetchall()
#     cursor1.close()
#     return render_template('largest.html', col=col, col1=col1)


# @app.route('/largedallas', methods=['GET', 'POST'])
# def largedallas():
#     radius = request.form['radius']
#     lat = request.form['latitude']
#     long1 = request.form['longitude']
#     north = float(lat) + float(radius) / 111
#     south = float(lat) - float(radius) / 111
#     east = float(long1) + float(radius) / 111
#     west = float(long1) - float(radius) / 111
#     connection = sql.connect("quakes.db")
#     cursor = connection.cursor()
#     query = "SELECT latitude, longitude, mag FROM quakes1 where latitude >= \'" + str(south) + "\' AND latitude <= \'" + str(north) + "\' AND longitude >= \'" + str(west) + "\'AND longitude <= \'" + str(east) + "\' order by mag desc limit 1"
#     cursor.execute(query)
#     col = cursor.fetchall()
#     cursor.close()
#     return render_template('largest.html', col=col)


# @app.route('/magni', methods=['GET', 'POST'])
# def magni():
#     st = request.form['start']
#     end = request.form['end']
#     connection = sql.connect("quakes.db")
#     cursor = connection.cursor()
#     query = "SELECT mag, time from quakes1 where mag >= \'" + str(st) + "\' AND mag <= \'" + str(end) + "\'"
#     cursor.execute(query)
#     col = cursor.fetchall()
#     row = []
#     count = 0
#     startdate = datetime.strptime('2020-06-10', '%Y-%m-%d')
#     for c in col:
#         timex = c[1].split("T")[0]
#         print(st)
#         if (datetime.strptime(timex, '%Y-%m-%d') > startdate):
#             count += 1
#             row.append(c)
#             print(end)
#     cursor.close()
#     return render_template('quakes.html', col=row, count = count)


# @app.route('/range', methods=['GET', 'POST'])
# def range():
#     radius = request.form['radius']
#     lat = request.form['latitude']
#     long1 = request.form['longitude']
#     north = float(lat) + float(radius) / 111
#     south = float(lat) - float(radius) / 111
#     east = float(long1) + float(radius) / 111
#     west = float(long1) - float(radius) / 111
#     r= float(radius)
#     connection = sql.connect("quakes.db")
#     cursor = connection.cursor()
#     query = "SELECT latitude, longitude, mag FROM quakes1 where latitude >= \'" + str(south) + "\' AND latitude <= \'" + str(north) + "\' AND longitude >= \'" + str(west) + "\'AND longitude <= \'" + str(east) + "\'"
#     cursor.execute(query)
#     out1 = cursor.fetchall()
    
#     query1 = "SELECT COUNT(latitude) FROM quakes1 where latitude >= \'" + str(south) + "\' AND latitude <= \'" + str(north) + "\' AND longitude >= \'" + str(west) + "\'AND longitude <= \'" + str(east) + "\'"
#     cursor.execute(query1)
#     out = cursor.fetchall()
#     ans=[]
#     print(out1)
#     for o in out1:
#         x=abs(o[0]-lat)
#         y=abs(o[1]-long1)
#         z=sqrt(x*x + y*y)
#         print(z,r)
#         if(z<=r):
#             ans.append(o)
#     print(ans)
#     return render_template('range.html', out=out, out1=ans)




# @app.route('/daterange', methods=['GET', 'POST'])
# def daterange():
#     mindate = request.form['mindate']
#     maxdate = request.form['maxdate']
#     connection = sql.connect("quakes.db")
#     cursor = connection.cursor()
#     query = "SELECT longitude, latitude, mag, time from quakes1 where mag > 3 "
#     cursor.execute(query)
#     col = cursor.fetchall()
#     row = []
#     count = 0
#     for c in col:
#         timex = c[3].split("T")[0]
#         if(timex >= mindate and timex <= maxdate):
#             count += 1
#             row.append(c)
#     cursor.close()
#     print(row.__len__())
#     return render_template('daterange.html', col=row, count = count)


# @app.route('/getRange', methods=['GET', 'POST'])
# def getRange():
#     fr = request.form['nm']
#     to = request.form['cpt']
#     connection = sql.connect("quakes.db")
#     cursor = connection.cursor()
#     query = "UPDATE quakes1 SET Caption = \'" + to + "\' where Name = \'" + fr + "\'"
#     cursor.execute(query)
#     connection.commit()
#     query1 = "Select name, picture, caption from quakes1 where name = \'" + fr + "\'"
#     cursor1 = connection.cursor()
#     cursor1.execute(query1)
#     entry = cursor1.fetchall()
#     cursor.close()
#     cursor1.close()
#     return render_template('test.html', entry=entry)


@app.route('/Question5')
def Question5():
    return render_template('selectv.html')

@app.route('/Question6')
def Question6():
    return render_template('tworange.html')

@app.route('/Question7')
def Question7():
    return render_template('sal.html')

@app.route('/Question8')
def Question8():
    return render_template('q8.html')

@app.route('/Question9')
def Question9():
    return render_template('q9.html')


port = int(os.getenv('PORT', '3000'))
app.run(host='0.0.0.0', port=port,debug=True)
