from flask import Flask
from routes.cases import case_routes
from routes.deaths import death_routes
app = Flask(__name__)

app.register_blueprint(case_routes)
app.register_blueprint(death_routes)

@app.route("/")
def hello_world():
    return "Hello World"
