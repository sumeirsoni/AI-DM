from pydantic import BaseModel
from typing import List
from datetime import datetime

class GameEvent(BaseModel):
    event_type: str
    narrative: str
    entities: List[str]
    location: str
    session: int
    importance: int
    timestamp: datetime = datetime.now()


if __name__ == "__main__":
    event = GameEvent(
        event_type="dialogue",
        narrative="Grimm says hello",
        entities=['grimm', 'party'],
        location="tavern",
        session=1
    )
    print(event)