from memory_manager import MemoryManager
from graph_client import GraphClient
from schemas import GameEvent

memory = MemoryManager()
graph = GraphClient()

graph.clear_all()
graph.close()

events = [
    GameEvent(
        event_type="arrival",
        narrative="The party enters the Rusty Tankard tavern. Old Grimm the dwarf bartender nods at them.",
        entities=["party", "grimm"],
        location="rusty_tankard",
        session=1,
        importance=5
    ),
    GameEvent(
        event_type="information",
        narrative="Grimm leans in and whispers: 'Bandits on the north road. They wear black cloaks and serve the Shadow Guild.'",
        entities=["grimm", "bandits", "shadow_guild"],
        location="rusty_tankard",
        session=1,
        importance=8
    ),
    GameEvent(
        event_type="combat",
        narrative="Three bandits burst through the door! After a fierce battle, the party defeats them.",
        entities=["party", "bandits"],
        location="rusty_tankard",
        session=1,
        importance=7
    )
]

for event in events:
    memory.store_event(event)

print("Loading scenario...")

print("\n" + "="*50)
print("Scenario loaded! Now begin the adventure...")

memory.ask_dm("What did Grimm tell us about the bandits?")
memory.ask_dm("Where are we right now?")

memory.get_entity_info("grimm")
memory.get_entity_info("bandits")
