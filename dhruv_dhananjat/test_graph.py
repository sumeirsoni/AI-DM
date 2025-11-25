from graph_client import GraphClient

graph = GraphClient()

graph.add_character("grimm", "Old Grimm", {"race": "Dwarf", "class": "Bartender"})

graph.add_location("rusty_tankard", "Rusty Tankard Tavern")

graph.add_relationship("grimm", "rusty_tankard", "WORKS_AT")

print("\n🔍 Grimm's relationships:")
relationships = graph.get_entity_relationships("grimm")
for rel in relationships:
    print(f"  - {rel['relationship']}: {rel['other_name']}")

graph.delete_char("grimm")
print("Deleted grimm node!")

graph.delete_loc("rusty_tankard")
print("Deleted the rusty tankard node!")

graph.close()
print("\n✅ Graph test complete!")