import cassandra.cluster as cs
import asyncio
import os
from datetime import datetime

cluster = cs.Cluster(['cassandra'], port=9042)

session = cluster.connect('local')


def log_event(db_name, message, tx_type):
    log_date = str(datetime.now())
    session.execute(f"insert into covid (id, db_name, log_message, transaction_date, transaction_type) values (uuid(),'{db_name}','{message}','{log_date}', '{tx_type}');")

