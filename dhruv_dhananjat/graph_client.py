import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from typing import List, Dict, Any

load_dotenv()

class GraphClient:

    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )

    def add_character(self, entity_id: str, name: str, properties: Dict[str, Any] = None):
        with self.driver.session() as session:
            props = properties or {}

            session.run(
                """
                MERGE (c:Character {id: $entity_id})
                SET c.name = $name, c+= $properties
                """,
                entity_id=entity_id,
                name=name,
                properties=props
            )
            print(f"Added character: {name}")
    
    def add_location(self, entity_id: str, name: str, properties: Dict[str, Any] = None):
        with self.driver.session() as session:
            props = properties or {}
            session.run(
                """
                MERGE (l:Location {id: $entity_id})
                SET l.name= $name, l += $properties
                """,
                entity_id=entity_id,
                name=name,
                properties=props
            )
            print(f"Added location: {name}")

    def add_relationship(self, from_id: str, to_id: str, rel_type: str):
        with self.driver.session() as session:
            session.run(
                f"""
                MATCH (a {{id: $from_id}}), (b {{id: $to_id}})
                MERGE (a)-[r: {rel_type}]->(b)
                """,
                from_id=from_id,
                to_id=to_id
            )
            print(f"Created relationship: {from_id} -{rel_type}-> {to_id}")
    
    def get_entity_relationships(self, entity_id: str) -> List[Dict[str, Any]]:
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (e {id: $entity_id})-[r]-(other)
                RETURN type(r) as relationship, other.id as id, other.name as other_name
                """,
                entity_id=entity_id
            )
            return [dict(record) for record in result]
        
    def delete_char(self, entity_id: str):
        with self.driver.session() as session:
            'MATCH (x:Character {id: $entity_id}) DETACH DELETE x'

    def delete_loc(self, entity_id: str):
        with self.driver.session() as session:
            'MATCH (x:Location {id: $entity_id}) DETACH DELETE x'
    
    def close(self):
        self.driver.close()