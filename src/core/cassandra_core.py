import cassandra.cluster as cs
import asyncio
import os
from datetime import datetime

cluster = cs.Cluster(['localhost'], port=7000)

session = cluster.connect('ssi')


async def log_event(db_name, message, tx_type):
    log_date = str(datetime.now())
    stmt = session.execute(f"insert into transactions (transaction_id, db_name, log_message, transaction_date, transaction_type) values (uuid(),'{db_name}','{message}','{log_date}', '{tx_type}' );")

