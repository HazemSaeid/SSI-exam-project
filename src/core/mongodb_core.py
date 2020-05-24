from pymongo import MongoClient
from bson.json_util import dumps
import pandas as pd

client = MongoClient()
db = client.local


def add_initial_covid_data():
    data = pd.read_csv('../resources/us-counties.csv')

    db.cases.insert_many(data.to_dict('records'))


def total_cases_by_date():
    data = db.cases.aggregate([
        {
            "$group": {
                "_id": "$date",
                "total_cases": {"$sum": "$cases"}
            }
        },
        {"$sort": {"total_cases": -1}}
    ])

    return dumps(data)


def total_cases_in(key, value):
    data = db.cases.aggregate([
        {
            "$match": {key: value}
        },
        {
            "$group": {
                "_id": f"${key}",
                "total_cases": {"$sum": "$cases"}
            }
        }
    ])

    return dumps(data)


def cases_history_in(key, value):
    data = db.cases.aggregate([
        {
            "$match": {key: value}
        },
        {
            "$group": {
                "_id": {
                    key: f"${key}",
                    "date": "$date"
                },
                "total_cases": {"$sum": "$cases"}
            }
        },
        {"$sort": {"_id.date": -1}}
    ])

    return dumps(data)


def total_deaths_by_date():
    data = db.cases.aggregate([
        {
            "$group": {
                "_id": "$date",
                "total_deaths": {"$sum": "$deaths"}
            }
        },
        {"$sort": {"total_deaths": -1}}
    ])

    return dumps(data)


def total_deaths_in(key, value):
    data = db.cases.aggregate([
        {
            "$match": {key: value}
        },
        {
            "$group": {
                "_id": f"${key}",
                "total_deaths": {"$sum": "$deaths"}
            }
        }
    ])

    return dumps(data)


def deaths_history_in(key, value):
    data = db.cases.aggregate([
        {
            "$match": {key: value}
        },
        {
            "$group": {
                "_id": {
                    key: f"${key}",
                    "date": "$date"
                },
                "total_deaths": {"$sum": "$deaths"}
            }
        },
        {"$sort": {"_id.date": -1}}
    ])

    return dumps(data)


# add_initial_covid_data()
# print(total_cases_by_date())
# print(cases_history_in('state', 'Washington'))
# print(cases_history_in('county', 'Orange'))
# print(total_cases_in('state', 'California'))
# print(total_cases_in('county', 'Los Angeles'))

# print(total_deaths_by_date())
# print(deaths_history_in('state', 'Washington'))
# print(deaths_history_in('county', 'Orange'))
# print(total_deaths_in('state', 'California'))
# print(total_deaths_in('county', 'Orange'))
