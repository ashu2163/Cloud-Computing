from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
import os
import re
from collections import Counter
import sqlite3 as sql
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask_bootstrap import Bootstrap

# EB looks for an 'application' callable by default.
application = Flask(__name__)
bootstrap = Bootstrap(application)
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'
myCount = 0


@application.route('/', methods=['GET', 'POST'])
def index():
    # data = []
    # connection = sql.connect("./earthquake.db")
    # cursor = connection.cursor()
    # query = "SELECT * FROM ssw"
    # cursor.execute(query)
    # rows = cursor.fetchall()
    # if rows is not None:
    #     for row in rows:
    #         data.append(row[0])
    # result = []
    # alamo = re.findall('\w+', open('Alamo.txt', encoding="utf8").read().lower())
    # for w in data:
    #     if w in alamo:
    #         result.append(w)
    # finalData = set(result)
    return render_template('index.html')


@application.route('/maxfreq', methods=['GET', 'POST'])
def maxfreq():
    n=int(request.form['n'])
    text = re.findall('\w+', open('l.txt', encoding="utf8").read().lower()) 
    d=Counter(text).most_common(n)

    text1 = re.findall('\w+', open('h.txt', encoding="utf8").read().lower()) 
    d1=Counter(text1).most_common(n)

    return render_template('q6.html',d=d,d1=d1)

@application.route('/removeWord', methods=['GET', 'POST'])
def removeWord():
    n=int(request.form['n'])
    text = re.findall('\w+', open('stopwords.txt', encoding="utf8").read().lower())
    
    text1 = re.findall('\w+', open('l.txt', encoding="utf8").read().lower())
    text2 = re.findall('\w+', open('h.txt', encoding="utf8").read().lower())
    count1=0
    count2=0
    for i in text:
        if i in text1:
            count1=count1+1
        if i in text2:
            count2=count2+1

    text1=open('l.txt','r')
    line=text1.readlines()

    result1 = ""
    for l in line:
        for w in text:
            l.replace(w, "")
        result1 += l

    text2=open('h.txt', encoding="utf8")
    line=text2.readlines()
    result2 = ""
    for l in line:
        for w in text:
            l.replace(w, "")
        result2 += l
    
    text1 = re.findall('\w+', open('l.txt', encoding="utf8").read().lower()) 
    for i in text1:
        if i in text1:
            text1.remove(i)
    d=Counter(text1).most_common(n)

    text2 = re.findall('\w+', open('h.txt', encoding="utf8").read().lower()) 
    for i in text:
        if i in text2:
            text2.remove(i)
    d2=Counter(text2).most_common(n)

    #print(d1)
    return render_template('q7.html',c1=count1,c2=count2, r1= result1, r2=result2, d=d,d2=d2)

# @application.route('/commonwords', methods=['GET', 'POST'])
# def commonWords():  
#     text = re.findall('\w+', open('Alamo.txt', encoding="utf8").read().lower()) 
#     connection = sql.connect("quakes.db")
#     cursor = connection.cursor()
#     query = "SELECT * FROM ssw"
#     cursor.execute(query)
#     words = cursor.fetchall()
#     d=[]
#     if words is not None:
#         for r in words:
#             d.append(r[0])
#     result=[]
#     for a in d:
#         if a in text:
#             result.append(a)
#     return render_template('index.html',r=result)


@application.route('/findbigram', methods=['GET', 'POST'])
def findbigram():
    word1=(request.form['w1'])
    word2=(request.form['w2'])
    
    text = re.findall('\w+', open('l.txt', encoding="utf8").read().lower())
    bi=Counter(zip(text, text[1:]))
    s=""
    a=0
    for i in bi:
        if i[0]==word1 and i[1]==word2:
            s=i[0]+" "+i[1]
            print(s)
            a=bi[i]

    text = re.findall('\w+', open('h.txt', encoding="utf8").read().lower())
    bi=Counter(zip(text, text[2:]))
    s1=""
    
    b=0
    for i in bi:
        if i[0]==word1 and i[1]==word2:
            s1=i[0]+" "+i[1]
            b=bi[i]

    return render_template('q8.html',ans=s,a=a,ans1=s1,b=b)


@application.route('/Question6')
def Question6():
    return render_template('q6.html')

@application.route('/Question7')
def Question7():
    return render_template('q7.html')

@application.route('/Question8')
def Question8():
    return render_template('q8.html')



# @application.route('/freq', methods=['GET', 'POST'])
# def freq():
#     # Open the file in read mode
#     text = re.findall('\w+', open('Alamo.txt').read().lower())
#     print(text)

#     print(os)
#     # Create an empty dictionary
#     d = {}

#     # Loop through each line of the file

#     # Iterate over each word in line
#     for word in text:
#         # Check if the word is already in dictionary*
#         if word in d:
#             # Increment count of word by 1
#             d[word] = d[word] + 1
#         else:
#             # Add the word to dictionary with count 1
#             d[word] = 1

#     sort_orders = dict(sorted(d.items(), key=lambda x: x[1], reverse=True))

#     text2 = open("Alamo.txt", "r")
#     d1 = {}

#     for line in text2:
#         line = line.strip()
#         line = line.lower()
#         words = line.split(" ")

#         for word in words:
#             if word in d1:
#                 d1[word] = d1[word] + 1
#             elif word:
#                 d1[word] = 1
#             # i=i-1
#     words = re.findall('\w+', open('Alamo.txt').read())
#     print(Counter(zip(d1, words[2:])))

#     sort_orders1 = dict(sorted(d1.items(), key=lambda x: x[1], reverse=True))
#     return render_template('index.html', dict=sort_orders, dict2=d1, dict3=sort_orders1, os=os.listdir(os.getcwd()))


# @application.route('/q61', methods=['GET', 'POST'])
# def q61():
#     list = []
#     # now = datetime.now()

#     # current_time = now.strftime("%H:%M:%S")
#     connection = sql.connect("earthquake.db")
#     cursor = connection.cursor()
#     query1 = "SELECT * from ssw"

#     cursor.execute(query1)
#     col = cursor.fetchall()
#     cursor.close()

#     for i in col:
#         list.append(i[0])
#     print(list)
#     text2 = re.findall('\w+', open('Alamo.txt').read().lower())
#     d1 = {}

#     # for line in text2:
#     #     line = line.strip()
#     #     line = line.lower()
#     #     words = line.split(" ")

#     for word in text2:
#         if word in list and word in d1:
#             d1[word] = d1[word] + 1
#         elif word in list:
#             d1[word] = 1
#     return render_template('index.html', out=d1)


# @application.route('/q8', methods=['GET', 'POST'])
# def q8():
#     freq = int(request.form['freq'])
#     data = []
#     connection = sql.connect("./earthquake.db")
#     cursor = connection.cursor()
#     query = "SELECT * FROM ssw"
#     cursor.execute(query)
#     rows = cursor.fetchall()

#     if rows is not None:
#         for row in rows:
#             data.append(row[0])
#     result = []
#     #sort_orders = {}
#     i = 0
#     alamo = re.findall('\w+', open('Alamo.txt', encoding="utf8").read().lower())
#     for w in data:
#         if w in alamo:
#             result.append(w)
#         # else:
#         #     result[w] = 1

#     #sort_orders = dict(sorted(result.items(), key=lambda x: x[1]))

#     return render_template('index.html', out=Counter(result).most_common()[:-freq - 1:-1])


# @application.route('/q10', methods=['GET', 'POST'])
# def q10():
#     new = []
#     with open("Alamo.txt", encoding="utf8") as fp:
#         for line in fp:
#             lines = line.lower().strip().split(".")
#             for i in lines[:-1]:
#                 new.append(i)
#     print(new)

#     name = str(request.form['name'])
#     print(name)
#     sentence = []
#     for i in new:
#         print(i)
#         if name in i:
#             sentence.append(i)
#     if len(sentence) != 0:
#         return render_template('index.html', word=sentence)
#     else:
#         return "NO sentence Found"


# @application.route('/q9', methods=['GET', 'POST'])
# def q9():
#     new = []
#     with open("Alamo.txt", encoding="utf8") as fp:
#         for line in fp:
#             lines = line.lower().strip().split(".")
#             for i in lines[:-1]:
#                 new.append(i)
#     sentence = []
#     for i in new:
#         if "1836" in i or "1834" in i or "1835" in i:
#             sentence.append(i)
#     return render_template('index.html', sentence=sentence)


# @application.route('/calculator', methods=['GET', 'POST'])
# def calculator():
#     num1 = int(request.form['num1'])
#     num2 = int(request.form['num2'])
#     opt = request.form['operator']
#     result = 1
#     factorial1 = 1
#     factorial2 = 1

#     if opt == 'Addition':
#         result = num1 + num2
#     elif opt == 'subtraction':
#         result = num1 - num2
#     elif opt == 'Multiplication':
#         result = num1 * num2
#     elif opt == 'Division':
#         result = num1 / num2
#     elif opt == 'Modulo':
#         result = num1 % num2
#     elif opt == 'Factorial':
#         for i in range(1, num1 + 1):
#             factorial1 = factorial1 * i
#         for i in range(1, num2 + 1):
#             factorial2 = factorial2 * i
#         return render_template('index.html', factorial1=factorial1, factorial2=factorial2, now=now)
#     return render_template('index.html', result=float(result), now=now)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
