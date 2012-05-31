# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template

from sqlalchemy import create_engine

engine = create_engine('mysql://root@localhost/', encoding='utf-8')

# Flask Application
app = Flask(__name__)

@app.route('/')
def index():
    connection = engine.connect()
    results = connection.execute('show processlist')
    for row in results.fetchall():
        print row
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
