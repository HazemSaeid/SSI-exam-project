import cassandra.cluster as cs
import asyncio
import os
from datetime import date

cluster = cs.Cluster(['127.0.0.1'], port=9042)

session = cluster.connect('ssi')


async def log_event(db_name, message, tx_type):
    ip_address = '127.0.0.1'
    log_date = str(date.today())
    stmt = session.execute(f"insert into transactions (transaction_id, db_name, log_message, transaction_date, transaction_type) values (uuid(),'{db_name}','{message}','{log_date}', '{tx_type}' );")

