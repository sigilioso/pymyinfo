# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template

from db_timer_manager import DatabaseTimerManager

dbt = DatabaseTimerManager('localhost', 'root', '')

# Flask Application
app = Flask(__name__)

@app.route('/')
def index():
    with dbt.execute('show processlist') as results:
        for row in results.fetchall():
            print row
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
