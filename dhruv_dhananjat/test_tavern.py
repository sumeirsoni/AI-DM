from memory_manager import MemoryManager
from schemas import GameEvent

memory = MemoryManager()

event1 = GameEvent(
    event_type="arrival",
    narrative="The party enters the Rusty Tankard tavern. Old Grimm the dwarf bartender nods at them.",
    entities=["party", "grimm"],
    location="rusty_tankard",
    session=1,
    importance=5
)

event2 = GameEvent(
    event_type="information",
    narrative="Grimm leans in and whispers: 'Bandits on the north road. They wear black cloaks and serve the Shadow Guild.'",
    entities=["grimm", "bandits", "shadow_guild"],
    location="rusty_tankard",
    session=1,
    importance=8
)

event3 = GameEvent(
    event_type="combat",
    narrative="Three bandits burst through the door! After a fierce battle, the party defeats them.",
    entities=["party", "bandits"],
    location="rusty_tankard",
    session=1,
    importance=7
)

for event in [event1, event2, event3]:
    memory.store_event(event)

print("\n" + '='*50)

queries = [
    "What did Grimm tell us?",
    "What happened with the bandits?",
    "Who is the Shadow Guild?"
]

for query in queries:
    print(f"\nQ: {query}")
    results = memory.search(query, limit=2)
    for r in results[:2]:
        print(f"  → {r['content'][:80]}...")