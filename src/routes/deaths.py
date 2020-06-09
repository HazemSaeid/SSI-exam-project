from flask import Blueprint
import core.neo4j_core as cn

death_routes = Blueprint('death_routes', __name__)


@death_routes.route("/deaths")
def get_total_death_cases_statistics():
    return cn.get_total_death_cases_statistics()


@death_routes.route("/deaths/<state>")
@death_routes.route("/deaths/<state>/<county>")
def total_death_cases_in(state, county=None):
    return cn.total_death_cases_in(state, county)


@death_routes.route("/deaths/<state>")
@death_routes.route("/deaths/<state>/<county>")
def total_death_cases_historical(state, county=None):
    return cn.total_death_cases_historical(state, county)
