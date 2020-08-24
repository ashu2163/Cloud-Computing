
import sqlite3 as sql
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from multiprocessing import Value
from flask_bootstrap import Bootstrap
import sqlite3 as sql
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


@application.route('/q6', methods=['GET', 'POST'])
def q6():
    name = request.form['name']
    
    return render_template('q7.html',name=name)



@application.route('/Question6')
def Question6():
    return render_template('q6.html')

# @application.route('/Question7')
# def Question7():
#     return render_template('q7.html')

# @application.route('/Question8')
# def Question8():
#     return render_template('q8.html')



if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
