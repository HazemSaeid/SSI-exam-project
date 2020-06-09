from flask import Flask, jsonify, request
import core.mongodb_core as cm
import core.neo4j_core as cn
from routes.cases import case_routes
from routes.deaths import death_routes
import psycopg2
app = Flask(__name__)
app.debug = True

app.register_blueprint(case_routes)
app.register_blueprint(death_routes)


@app.route('/refresh')
def sync_data():
    return cn.sync_data()


@app.route('/')
def hello_world():
    return cm.add_initial_covid_data()
