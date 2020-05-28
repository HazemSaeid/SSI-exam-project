from flask import Blueprint
import core.mongodb_core as cm

death_routes = Blueprint('death_routes', __name__)


@death_routes.route("/deaths")
def total_deaths_by_date():
    return cm.total_deaths_by_date()


@death_routes.route("/deaths/<key>/<value>/history")
def deaths_history_in(key, value):
    return cm.deaths_history_in(key, value)


@death_routes.route("/deaths/<key>/<value>")
def total_deaths_in(key, value):
    return cm.total_deaths_in(key, value)
