# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
import MySQLdb

db = MySQLdb.connect('localhost', user='root', passwd='')
cursor = db.cursor()

# Flask Application
app = Flask(__name__)

@app.route('/')
def index():
    cursor.execute('SHOW PROCESSLIST')
    for row in cursor.fetchall():
        print row
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
