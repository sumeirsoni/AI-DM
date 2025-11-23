import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
)

with driver.session() as session:
    result = session.run(
        "CREATE (c.Character {name: 'Test Hero', race: 'Human}) RETURN C"
    )
    print("Created:", result.single()[0])

    result = session.run("MATCH (c.Character {name: 'Test Hero'}) RETURN c")
    print("Found:", result.single()[0])

    session.run("MATCH (c.Character {name: 'Test Hero'}) DELETE c")
    print("Cleaned up")

driver.close()
print("Neo4j connection working!")