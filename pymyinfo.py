# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template, make_response
from flask import jsonify
from flask import request

from db_timer_manager import DatabaseTimerManager

from settings import HOST, USER, PASSWORD

# Stablish the MySQL configuration
dbt = DatabaseTimerManager(HOST, USER, PASSWORD)

# Flask Application
app = Flask(__name__)

@app.route('/')
def process_list():
    """
    Render the index (process list) page.
    """
    return render_template('index.html')

@app.route('/configuration')
def configuration():
    """
    Get some server configuration info and render the configuration page.
    """
    server_info = {}
    with dbt.execute('show variables') as results:
        server_info = dict([(r['Variable_name'], r['Value']) for r in results])
    return render_template('configuration.html', server_info=server_info)

@app.route('/mypci')
def json_mysql_process_list():
    """
    Returns the MySQL processlist information by means of a JSON.
    """
    process_list_info = []
    with dbt.execute('show full processlist') as results:
        process_list_info = list(results.fetchall())
    return jsonify(process_list_info=process_list_info)

@app.route('/killprocess', methods=['POST'])
def kill_process():
    """
    Tris to kill the process corresponding to the pid posted.
    """
    if request.method == 'POST':
        pid = request.form['pid']
        try :
            with dbt.execute('kill %s', pid): pass
        except :
            pass
        return make_response('', 200)
    return make_response('', 401)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
