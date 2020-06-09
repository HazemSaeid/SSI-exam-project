import py2neo as neo
from redis import Redis
from redis_cache import RedisCache
from bson.json_util import dumps

graph = neo.Graph("bolt://neo4j:7687", auth=("neo4j", "12345"))

r_client = Redis(host="redis", port=6379)
cache = RedisCache(redis_client=r_client)


def sync_data():
    try:
        graph.run("""
        :auto USING PERIODIC COMMIT 500
        LOAD CSV WITH HEADERS FROM "file:///covid.csv" AS row
        MERGE (c:County {name: row.county, state: row.state})
        CREATE (d:Date {date: row.date, amount: row.cases, deaths: row.deaths})
        MERGE (c)-[rsd:ON]->(d)
        """)

        return 'neo4j data up to date'
    except:
        return 'An exception occurred'


# @cache.cache(ttl=900)
def total_cases_in(state):
    data = graph.run(
        f"MATCH(s:State) WHERE s.name = '{state}' RETURN s.name as state, SUM(toInteger(s.amount)) as total_cases")

    return dumps(data)

# @cache.cache(ttl=900)
# def cases_history_in(state):
#     data = graph.run(f"MATCH(s:State) WHERE s.name = '{state}' RETURN s.name as state, SUM(toInteger(s.amount)) as total_cases")

#     return dumps(data)
