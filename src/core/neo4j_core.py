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
        MERGE (s: State {name: row.state})
        MERGE (c:County {name: row.county, state: row.state})
        CREATE (d:Cases {date: row.date, amount: row.cases, deaths: row.deaths})
        MERGE (c)-[rsd:ON]->(d)
        MERGE (s)-[r:HAS]->(c)
        """)

        graph.run("CREATE INDEX state_name for (s:State) on (s.name)")
        graph.run("CREATE INDEX county_name for (c:County) on (c.name)")

        return 'neo4j data up to date'
    except:
        return 'An exception occurred'


@cache.cache(ttl=900)
def get_total_cases_statistics():
    data = graph.run(f"match (c:Cases) return SUM(toInteger(c.amount)) as total_cases, c.date as date order by date asc")

    return dumps(data)


@cache.cache(ttl=900)
def total_cases_in(state, county=None):
    if(county != None):
        data = graph.run(f"match (c:County)-[:ON]->(ca:Cases) where c.state = '{state}' and c.name = '{county}' return SUM(toInteger(ca.amount)) as total_cases")
    else:
        data = graph.run(f"match (c:County)-[:ON]->(ca:Cases) where c.state = '{state}' return SUM(toInteger(ca.amount)) as total_cases")

    return dumps(data)


@cache.cache(ttl=900)
def total_cases_historical(state, county=None):
    if(county != None):
        data = graph.run(f"match (c:County)-[:ON]->(ca:Cases) where c.state = '{state}' and c.name = '{county}' return SUM(toInteger(ca.amount)) as total_cases, ca.date as date order by date asc")
    else:
        data = graph.run(f"match (c:County)-[:ON]->(ca:Cases) where c.state = '{state}' return SUM(toInteger(ca.amount)) as total_cases, ca.date as date order by date asc")

    return dumps(data)


@cache.cache(ttl=900)
def get_total_death_cases_statistics():
    data = graph.run(f"match (ca:Cases) return SUM(toInteger(ca.deaths)) as total_deaths , ca.date as date order by date asc")

    return dumps(data)


@cache.cache(ttl=900)
def total_death_cases_in(state, county=None):
    if(county != None):
        data = graph.run(f"match (c:County)-[:ON]->(ca:Cases) where c.state = '{state}' and c.name = '{county}' return SUM(toInteger(ca.deaths)) as total_deaths")
    else:
        data = graph.run(f"match (c:County)-[:ON]->(ca:Cases) where c.state = '{state}' return SUM(toInteger(ca.deaths)) as total_deaths")

    return dumps(data)


@cache.cache(ttl=900)
def total_death_cases_historical(state, county=None):
    if(county != None):
        data = graph.run(f"match (c:County)-[:ON]->(ca:Cases) where c.state = '{state}' and c.name = '{county}' return SUM(toInteger(ca.deaths)) as total_deaths , ca.date as date order by date asc")
    else:
        data = graph.run(f"match (c:County)-[:ON]->(ca:Cases) where c.state = '{state}' return SUM(toInteger(ca.deaths)) as total_deaths , ca.date as date order by date asc")

    return dumps(data)