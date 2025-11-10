import os
from dotenv import load_dotenv
from supermemory import Supermemory
from schemas import GameEvent

load_dotenv()

class MemoryManager():
    def __init__(self):
        self.client = Supermemory(
            api_key=os.getenv("SUPERMEMORY_API_KEY"),
            base_url="https://api.supermemory.ai/"
        )

        self.current_session = 1

    def store_event(self, event: GameEvent):
        print(f"Storing event: {event.event_type}")

        result = self.client.memories.add(
            content = event.narrative,
            container_tags = [f"session-{event.session}", event.location],
            metadata={
                'event_type': event.event_type,
                'entities': event.entities,
                'importance': event.importance,
                'location': event.location
            }
        )

        print(f"Stored with id: {result.id}")
        return result.id
    
    def search(self, query: str, limit):
        print(f"Seaching: {query}")

        search_result = self.client.search.memories(
            q= query,
            limit= limit
        )

        return search_result
