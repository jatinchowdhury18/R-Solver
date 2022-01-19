from flask import Flask, request, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from collections import namedtuple

import sys
sys.path.insert(0, './')
from r_solver import main as r_solver

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = app.root_path + '/uploads/'
app.config['netlist_file'] = None
app.config['scatt_file'] = None

@app.route('/rsolver')
def my_form():
    return render_template("r_solver.html")

@app.route('/rsolver/upload_netlist', methods=['POST'])
def do_post():
    try:
        netlist_file = request.files['file']
        netlist_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(netlist_file.filename)))
        app.config['netlist_file'] = netlist_file
        return render_template("r_solver.html", netlist_file=netlist_file.filename)
    except:
        print('Unable to upload file!')
        pass
    
    return render_template("r_solver.html")

@app.route('/rsolver/solve', methods=['POST'])
def do_solve():
    netlist = app.config['netlist_file']
    if netlist is None:
        return render_template("r_solver.html")

    app.config['scatt_file'] = netlist.filename.split('.')[0] + '_scatt.txt'

    netlist_file = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(netlist.filename))
    out_file = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(app.config['scatt_file']))

    Args = namedtuple('Args', ['netlist', 'datum', 'adapted_port', 'out_file', 'verbose'])
    args = Args(
        datum = int(request.form['datum']),
        adapted_port = int(request.form['adapt']),
        verbose = False,
        out_file = open(out_file, 'w'),
        netlist = open(netlist_file, 'r')
    )

    r_solver(args, custom_args=True)
    
    return render_template("r_solver.html",
                           netlist_file=app.config['netlist_file'].filename,
                           scatt_file=app.config['scatt_file'])

@app.route('/rsolver/download')
def do_get():
    return send_from_directory(app.config['UPLOAD_FOLDER'],
        secure_filename(app.config['scatt_file']), as_attachment=True)

if __name__ == '__main__':
    app.run(port=220, ssl_context='adhoc', debug=False)
