from flask import Flask
from flask import abort, redirect, url_for, request, Response
import requests
app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/static/select/', methods=['GET'])
def search():
    payload = request.args
    r = requests.get('http://localhost:8983/solr/ir_project/select', params=payload)
    return r.text