from flask import Blueprint
import core.neo4j_core as cn

case_routes = Blueprint('case_routes', __name__)


@case_routes.route("/cases")
def get_total_cases_statistics():
    return cn.get_total_cases_statistics()


@case_routes.route("/cases/<state>")
@case_routes.route("/cases/<state>/<county>")
def total_cases_in(state, county=None):
    return cn.total_cases_in(state, county)


@case_routes.route("/cases/<state>")
@case_routes.route("/cases/<state>/<county>")
def total_cases_historical(state, county=None):
    return cn.total_cases_historical(state, county)
