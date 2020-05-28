from flask import Blueprint
import core.mongodb_core as cm

case_routes = Blueprint('case_routes', __name__)


@case_routes.route("/cases")
def total_cases_by_date():
    return cm.total_cases_by_date()


@case_routes.route("/cases/<key>/<value>/history")
def cases_history_in(key, value):
    return cm.cases_history_in(key, value)


@case_routes.route("/cases/<key>/<value>")
def total_cases_in(key, value):
    return cm.total_cases_in(key, value)
