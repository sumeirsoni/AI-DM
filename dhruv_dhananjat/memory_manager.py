import os
from dotenv import load_dotenv
from supermemory import Supermemory
from schemas import GameEvent
from anthropic import Anthropic

load_dotenv()

class MemoryManager():
    def __init__(self):
        self.client = Supermemory(
            api_key=os.getenv("SUPERMEMORY_API_KEY"),
            base_url="https://api.supermemory.ai/"
        )

        self.ai = Anthropic(api_key = os.getenv("ANTHROPIC_API_KEY"))

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
    
    def ask_dm(self, question: str):
        print(f"\nPLayer asks: {question}")

        memories = self.search(question, limit=3)
        
        context = "Here's what happened in the game:\n\n"
        
        for i, result in enumerate(memories, 1):
            context += f"{i}. {result.memory}\n"

        response = self.ai.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": "You are a Dungeon Master. use this context to answer the player's question"
            }]
        )

        dm_response =response.content[0].text
        print(f"DM: {dm_response}")
        return dm_response
