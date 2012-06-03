# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import jsonify

from db_timer_manager import DatabaseTimerManager

dbt = DatabaseTimerManager('localhost', 'root', '')

# Flask Application
app = Flask(__name__)

@app.route('/')
def index():
    server_info = {}
    with dbt.execute('show variables') as results:
        server_info = dict([(r['Variable_name'], r['Value']) for r in results])
    return render_template('index.html', server_info=server_info)

@app.route('/mypci')
def json_mysql_process_list():
    process_list_info = []
    with dbt.execute('show processlist') as results:
        process_list_info = list(results.fetchall())
    return jsonify(process_list_info=process_list_info)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
    app.run()
