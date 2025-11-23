from graph_client import GraphClient

graph = GraphClient()

graph.add_character("grimm", "Old Grimm", {"race": "Dward", "class": "Bartender"})

graph.add_location("rusty_tankard", "Rusty Tankard Tavern")

graph.add_relationship("grimm", "rusty_tankard", "WORKS_AT")

print("\n🔍 Grimm's relationships:")
relationships = graph.get_entity_relationships("grimm")
for rel in relationships:
    print(f"  - {rel['relationship']}: {rel['other_name']}")

graph.close()
print("\n✅ Graph test complete!")