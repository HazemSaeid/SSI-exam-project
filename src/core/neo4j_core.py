import py2neo as neo

graph = neo.Graph("bolt://neo4j:7687", auth=("neo4j", "12345"))


def sync_data():
    try:
        graph.run("""
        USING PERIODIC COMMIT 1000
        LOAD CSV WITH HEADERS FROM "file:///covid.csv" AS row
        MERGE (s:State {name: row.state})
        MERGE (c:Cases {date: row.date, amount: row.cases, deaths:row.deaths})
        MERGE (co:County {name: row.county})
        MERGE (s)-[h:HAS]->(c)
        MERGE (c)-[r:REGISTERED]->(co)
        """)

        return 'neo4j data up to date'
    except:
        return 'An exception occurred'
