from flask import Flask
import core.mongodb_core as cm
from routes.cases import case_routes
from routes.deaths import death_routes
app = Flask(__name__)


app.register_blueprint(case_routes)
app.register_blueprint(death_routes)


@app.route("/")
def hello_world():
    return cm.add_initial_covid_data()
