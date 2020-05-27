import py2neo as neo
import asyncio
from objects.objects import CovidCase

graph = neo.Graph("bolt://localhost:7687", auth=("neo4j","12345"))

#async def insert_csv_data():
    #stmt = """ 
    #LOAD CSV WITH HEADERS FROM src\resources\us-counties.csv AS row 
    #MERGE (s:State {state: row.name})
    #MERGE (c:Cases {date: row.date, amount: row.amount, deaths:row.deaths})
    #MERGE (co:County {name: row.county})
    #"""


async def add_covid_data(_state, _county,_date, _cases, _deaths):
    tx = graph.begin()
    state = neo.Node("State", name = _state )
    county = neo.Node("County", name = _county)
    cases = neo.Node("Cases", date= _date, amount = _cases, deaths = _deaths)

    state_rel_county = neo.Relationship(state, "HAS", county)
    county_rel_cases = neo.Relationship(county, "REGISTERED", cases)

    tx.merge(state, primary_label="State", primary_key=("name"))
    tx.merge(county,primary_label="County", primary_key=("name"))
    tx.merge(state_rel_county, primary_label="HAS", primary_key=("state","county"))
    tx.create(cases)
    tx.create(county_rel_cases)
    tx.commit()

async def get_cases_from_county(_county):
    tx = graph.begin()
    stmt = graph.run(f"MATCH (c:County)-[r:REGISTERED]-(ca:Cases) where c.name = '{_county}' RETURN  ca limit 5000").data()



#asyncio.run(add_covid_data("h","Orange County","dsa",12,22))
#asyncio.run(get_cases_from_county("Orange County"))