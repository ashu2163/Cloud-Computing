
import sqlite3 as sql
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from multiprocessing import Value
from flask_bootstrap import Bootstrap
import random

# EB looks for an 'application' callable by default.
application = Flask(__name__)
bootstrap = Bootstrap(application)
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'
counter = Value('i', 0)
@application.route('/', methods=['GET', 'POST'])
def index():
    # with counter.get_lock():
    #     counter.value += 1
    #     out = counter.value

    #     return jsonify(count=out)
    return render_template('index.html', name=None)


@application.route('/barChart', methods=['GET', 'POST'])
def barChart1():
    country = request.form['country']
    col1 = [['Country','Volcano',{'role':'style'},{'role':'annotation'}]]
    connection = sql.connect("quakes.db")
    cursor = connection.cursor()
    query = "select VolcanoName,Elev from volcano where Country = '" + str(country) +"'"
    cursor.execute(query)
    col = cursor.fetchall()
    t_c = len(col)
    i=0
    while(i<t_c):
        random_number = random.randint(0,16777215)
        h_n = str(hex(random_number))
        h_n ='#'+ h_n[2:]
        col1.append([ col[i][0], col[i][1], h_n,col[i][0] ])
        i=i+1
    cursor.close()
    return render_template('barChart.html', col1=col1)


@application.route('/pieChart', methods=['GET', 'POST'])
def PieChart():
    fromElev = int(request.form['elev1'])
    toElev = int(request.form['elev2'])
    division = int(request.form['div1'])
    t_c = 0
    col1 = [['Elev','No Of Country',{'role':'style'}]]
    connection = sql.connect("quakes.db")
    cursor = connection.cursor()
    d = (float(toElev) - float(fromElev)) / float(division)
    division = int(division)
    fromElev = float(fromElev)
    while int(division) > 0:
        query = "select * from volcano where Elev >= " + str(fromElev) + " and Elev < " + str(float(fromElev) + float(d)) + ""
        cursor.execute(query)
        col = cursor.fetchall()
        magR = str(fromElev) + " to " + str(float(fromElev) + float(d))
        t_c = len(col)
        random_number = random.randint(0,16777215)
        h_n = str(hex(random_number))
        h_n ='#'+ h_n[2:]
        col1.append([ magR, t_c, h_n ])
        division -= 1
        fromElev += d

    cursor.close()

    return render_template('pieChart.html', col1=col1)


@application.route('/scatterChart', methods=['GET', 'POST'])
def ScatterChart():
    fromNum1 = int(request.form['vn1'])
    toNum2 = int(request.form['vn2'])
    t_c = 0
    col1 = [['Volcano range','Elevation',{'role':'style'}]]
    connection = sql.connect("quakes.db")
    cursor = connection.cursor()
    
    query = "select Number,Elev from volcano where Number >= '" + str(fromNum1) + "' and Number < '" + str(float(toNum2)) + "'"
    cursor.execute(query)
    col = cursor.fetchall()
    t_c=len(col)
    i=0
    while(i<t_c):
        #magR = str(fromNum1) + " to " + str(float(toNum2))
        random_number = random.randint(0,16777215)
        h_n = str(hex(random_number))
        h_n ='#'+ h_n[2:]
        col1.append([ col[i][0] , col[i][1], h_n ])
        i=i+1

    cursor.close()
    return render_template('ScatterChart.html', col1=col1)

@application.route('/Question6')
def Question6():
    return render_template('barChart.html')

@application.route('/Question7')
def Question7():
    return render_template('pieChart.html')

@application.route('/Question8')
def Question8():
    return render_template('ScatterChart.html')


# @application.route('/pieChart', methods=['GET', 'POST'])
# def pieChart():
#     fromMin = request.form['min1']
#     toMax = request.form['max1']
#     year = request.form['year']
#     total_count = 0
#     col1 = []
#     per = []
#     pop = 0
#     connection = sql.connect("earthquake.db")
#     print("connection")
#     cursor = connection.cursor()
#     query = "Select State, \"" + str(year) +"\" from sp where \"" + str(year) + "\" > \'" + str(fromMin) + "\' and \"" + str(year) + "\" < \'" + str(toMax) + "\'"
#     cursor.execute(query)
#     out1 = cursor.fetchall()
#     print(query)
#     print(out1)
#     total_part = len(out1)
#     for a in out1:
#         pop += int(a[1].replace(',',''))


#     map = {}

#     print(pop)
#     print(total_part)
#     for c in out1:
#         state = c[0]
#         print("ok")
#         # state_count = c[1]

#         query1 = "select \"" + str(year) + "\", State from sp where State = \'" + str(state) + "\' and \"" + str(year) + "\" > \'" + str(fromMin) + "\' and \'" + str(year) + "\' < \'" + str(toMax) + "\'"
#         cursor.execute(query1)
#         out2 = cursor.fetchall()
#         x = (int(out2[0][0].replace(',','')) / pop * 100)
#         per.append(x)
#         if out2[0][1] in map:
#             map[out2[0][1]] += x
#         else:
#             map[out2[0][1]] = x

#     print(map)
#     for key in map:
#         col1.append({'magRange': map[key], 'count': key})

#     print(col1)
#     # d = (int(toMag) - int(fromMag)) / int(division)
#     # division = int(division)
#     # fromMag = float(fromMag)
#     # e = 2.6 + 0.20
#     # print(e)
#     # while int(division) > 0:
#     #     query = "select latitude, longitude, mag from quake where mag >= \'" + str(fromMag) + "\' and mag < \'" + str(fromMag + d) + "\' order by mag"
#     #     cursor.execute(query)
#     #     col = cursor.fetchall()
#     #     magRange = str(fromMag) + " to " + str(fromMag + d)
#     #     print(magRange)
#     #     total_count = len(col)
#     #     col1.append({'magRange': magRange, 'count': total_count})
#     #     division -= 1
#     #     fromMag += d
#     #
#     # cursor.close()


#     return render_template('pieChart.html', col1=col1)

# @application.route('/scatterChart', methods=['GET', 'POST'])
# def scatterChart():
#     fromMag = float(request.form['min_y'])
#     toMag = float(request.form['max_y'])

#     col1 = []
#     connection = sql.connect("earthquake.db")
#     print("connection")
#     cursor = connection.cursor()


#     query = "select State from sp where mag >= \'" + str(fromMag) + "\' and mag < \'" + str(toMag) + "\' order by mag"
#     cursor.execute(query)
#     col = cursor.fetchall()
#     for c in col:

#         year = c[0]
#         State = c[1]
#         mag = c[2]
#         col1.append({'Latitude': year, 'Longitude': State})


#     cursor.close()

#     return render_template('scatterChart.html', col1=col1)

# @application.route('/scatterChart1', methods=['GET', 'POST'])
# def scatterChart1():
#     fromYear = float(request.form['min_l'])
#     toYear = float(request.form['max_l'])
#     state = request.form['state']

#     col1 = []
#     connection = sql.connect("earthquake.db")
#     print("connection")
#     cursor = connection.cursor()
#     if fromYear > toYear:
#         temp = fromYear
#         fromYear = toYear
#         toYear = temp

#     if fromYear < 2010:
#         fromYear = 2010
#     if toYear > 2018:
#         toYear = 2018
#     map = {}
#     while fromYear < toYear:

#         query = "select \"" + str(int(fromYear)) + "\" from sp where State = \'" + str(state) + "\'"
#         cursor.execute(query)

#         col = cursor.fetchall()
#         print(col)
#         str1 = int(col[0][0].replace(',',''))
#         map[str(fromYear)] = str1
#         print(str1)
#         fromYear += 1

#     for key in map:
#         col1.append({'Latitude': key, 'Longitude': map[key]})

#     cursor.close()

#     return render_template('scatterChart.html', col1=col1)
# @application.route('/scatterChart3', methods=['GET', 'POST'])
# def scatterChart3():
#     fromYear = request.form['year1']
#     toYear = request.form['year2']
#     state = request.form['state']

#     col1 = []
#     connection = sql.connect("earthquake.db")
#     print("connection")
#     cursor = connection.cursor()
#     if fromYear > toYear:
#         temp = fromYear
#         fromYear = toYear
#         toYear = temp

#     if fromYear < 2010:
#         fromYear = 2010
#     if toYear > 2018:
#         toYear = 2018
#     map = {}
#     while fromYear < toYear:
#         query = "select \"" + str(fromYear) + "\" from sp where State = \'" + str(state) + "\'"
#         cursor.execute(query)
#         col = cursor.fetchall()
#         map[str(fromYear)] = col[0][0]
#         fromYear += 1

#     for key in map:
#         col1.append({'Latitude': key, 'Longitude': map[key]})

#     cursor.close()

#     return render_template('scatterChart.html', col1=col1)


# # @application.route('/scatterChart2', methods=['GET', 'POST'])
# # def scatterChart2():
# #     fromYear = request.form['min']
# #     toYear = request.form['max']
# #     state = request.form['state']
# #
# #
# #     col1 = []
# #     connection = sql.connect("earthquake.db")
# #     print("connection")
# #     cursor = connection.cursor()
# #     if fromYear > toYear:
# #         temp = fromYear
# #         fromYear = toYear
# #         toYear = temp
# #
# #     if fromYear < 2010:
# #         fromYear = 2010
# #     if toYear > 2018:
# #         toYear = 2018
# #     map={}
# #     while fromYear < toYear:
# #         query = "select \"" + str(fromYear) + "\" from sp where State = \'" + str(state) + "\'"
# #         cursor.execute(query)
# #         col = cursor.fetchall()
# #         map[str(fromYear)] = col[0][0]
# #         fromYear += 1
# #
# #     for key in map:
# #         col1.append({'Latitude': key, 'Longitude': map[key]})
# #
# #
# #     cursor.close()
# #
# #     return render_template('scatterChart.html', col1=col1)


# @application.route('/lineChart', methods=['GET', 'POST'])
# def lineChart():
#     fromMag = float(request.form['mag1'])
#     toMag = float(request.form['mag2'])

#     col1 = []
#     connection = sql.connect("earthquake.db")
#     print("connection")
#     cursor = connection.cursor()

#     query = "select mag from quake where mag >= \'" + str(fromMag) + "\' and mag < \'" + str(
#         toMag) + "\' order by mag"
#     cursor.execute(query)
#     col = cursor.fetchall()
#     total_count = len(col)
#     for c in col:

#         mag = c[0]
#         col1.append({'Latitude': mag, 'Longitude': total_count})

#     cursor.close()

#     return render_template('lineChart.html', col1=col1)

# run the app.


# @app.route('/Question9')
# def Question9():
#     return render_template('q9.html')


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
