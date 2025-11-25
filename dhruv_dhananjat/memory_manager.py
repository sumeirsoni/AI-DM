import os
from dotenv import load_dotenv
from supermemory import Supermemory
from schemas import GameEvent
from anthropic import Anthropic
from graph_client import GraphClient

load_dotenv()

class MemoryManager():
    def __init__(self):
        self.client = Supermemory(
            api_key=os.getenv("SUPERMEMORY_API_KEY"),
            base_url="https://api.supermemory.ai/"
        )
        self.graph = GraphClient()
        self.ai = Anthropic(api_key = os.getenv("ANTHROPIC_API_KEY"))

        self.current_session = 1

        self.current_state = {
            "location": None,
            "recent_npcs": [],
            "recent_events": [],
            "party_status": "active"
        }

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
        
        for entity in event.entities:
            if entity == "party":
                continue 
            elif "loc_" in entity or entity == event.location:
                self.graph.add_location(
                    entity_id=entity,
                    name=entity.replace("_", " ").title()
                )
            else:
                self.graph.add_character(
                    entity_id=entity,
                    name=entity.replace("_", " ").title()
                )

        for i, entity1 in enumerate(event.entities):
            if entity1 == "party":
                continue
            for entity2 in event.entities[i+1:]:
                if entity2 == "party":
                    continue
                self.graph.add_relationship(entity1, entity2, "KNOWS")

        self.current_state["location"] = event.location
        self.current_state["recent_events"].append(event.narrative)

        if len(self.current_state["recent_events"]) > 3:
            self.current_state["recent_events"].pop(0)
        
        for entity in event.entities:
            if entity != "party" and entity not in self.current_state["recent_npcs"]:
                self.current_state["recent_npcs"].append(entity)
        if len(self.current_state["recent_npcs"]) > 5:
            self.current_state["recent_npcs"].pop(0)
        
        print(f"   ✓ Stored in Supermemory: {result.id}")
        print(f"   ✓ Updated graph with {len(event.entities)} entities")
        
        return result.id
    
    def search(self, query: str, limit):
        print(f"Searching: {query}")

        search_result = self.client.search.memories(
            q= query,
            limit= limit
        )

        return search_result
    
    def delete(self, id):
        self.client.memories.delete(id)
    
    def ask_dm(self, question: str):
        print(f"\n💭 Player asks: {question}")
        
        memories = self.search(question, limit=3)
        
        context = "=== CURRENT GAME STATE ===\n"
        context += f"Location: {self.current_state['location']}\n"
        context += f"Recent NPCs: {', '.join(self.current_state['recent_npcs'])}\n"

        context += "\n=== ENTITY RELATIONSHIPS ===\N"
        for npc in self.current_satate['recent_npcs'][:3]:
            relationships = self.graph.get_entity_relationships(npc)
            if relationships:
                context += f"{npc.replace('_', ' ').title()}:\n"
                for rel in relationships[:3]:
                    context += f" - {rel['relationships']}: {rel['other_name']}\n"

        context += f"\n=== RECENT EVENTS ===\n"
        for event in self.current_state["recent_events"]:
            context += f"- {event}\n"
        
        context += f"\n=== RELEVANT MEMORIES ===\n"
        for result in memories.results:
            context += f"- {result.memory}\n"

        print(context)
        
        response = self.ai.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": f"""You are a Dungeon Master. Use this context to answer the player's question: {context}

                Player's question: {question}

                Answer as the DM, being helpful and staying true to what happened."""
            }]
        )
        
        dm_response = response.content[0].text
        print(f"\n🎲 DM: {dm_response}")
        return dm_response

    def get_entity_info(self, entity_id: str):
        print(f"Getting info for: {entity_id}")
        
        relationships = self.graph.get_entity_relationships(entity_id)

        print(f"Found {len(relationships)} relationships:")
        for rel in relationships:
            print(f" - {rel['relationship']}: {rel['other_name']}")

        return relationships