import couchdb
import csv
from objects.objects import CovidCase
from neo4j_core import add_covid_data
from redis_core import update_death_count
import asyncio
import json
import os

couch = couchdb.Server('http://admin:password@localhost:5984/')

db = couch['covid']

async def add_initial_data():
    with open(r"src\resources\us-counties.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        for line in reader:
            print ("added record from " + line[2])
            obj = CovidCase(line[0], line[1], line[2], line[3], int(line[4]), int(line[5]))
            db.save(obj.__dict__)
            print ("adding to neo4j")
            asyncio.run(add_covid_data(str(line[2]), str(line[1]),str(line[0]), int(line[4]), int(line[5])))
            asyncio.run(update_death_count(int(line[5])))

async def insert(obj: CovidCase):
    db.save(obj.__dict__)
    await update_death_count(int(obj.deaths))
    await add_covid_data(obj.state, obj.county, obj.date, obj.cases, obj.deaths)
    

async def get_death_count():
    item = db.view('cases_info/deaths')
    for i in item.rows:
        return i.value

covid_case = CovidCase("2020-05-14","Orange", "Texas", 2342, 227, 3133) 
asyncio.run(insert(covid_case))