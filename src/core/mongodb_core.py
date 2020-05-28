from redis import Redis
from redis_cache import RedisCache
from pymongo import MongoClient
from bson.json_util import dumps
import pandas as pd

m_client = MongoClient()
db = m_client.local

r_client = Redis(host="localhost", port=6379)
cache = RedisCache(redis_client=r_client)


def add_initial_covid_data():
    try:
        data = pd.read_csv('./resources/us-counties.csv')

        db.cases.insert_many(data.to_dict('records'))

        return 'The source data was added to MongoDB successfully.'
    except:
        return 'An exception occurred'


@cache.cache(ttl=900)
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


@cache.cache(ttl=900)
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


@cache.cache(ttl=900)
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


@cache.cache(ttl=900)
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


@cache.cache(ttl=900)
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


@cache.cache(ttl=900)
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
