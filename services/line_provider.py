import time
from copy import deepcopy
from fastapi import FastAPI, Path, HTTPException
from httpx import AsyncClient

from models import Event, EventState
from settings import BET_MAKER_API_BASE

events: dict[str, Event] = {
    '1': Event(event_id='1', coefficient=1.2, deadline=int(time.time()) + 600, state=EventState.NEW),
    '2': Event(event_id='2', coefficient=1.15, deadline=int(time.time()) + 60, state=EventState.NEW),
    '3': Event(event_id='3', coefficient=1.67, deadline=int(time.time()) + 90, state=EventState.NEW),
    '4': Event(event_id='4', coefficient=1.89, deadline=int(time.time()) + 300, state=EventState.NEW),
    '5': Event(event_id='5', coefficient=1.11, deadline=int(time.time()) + 300, state=EventState.NEW)
}

app = FastAPI()


@app.put('/event')
async def create_event(event: Event) -> dict:
    """
        Создание/Изменение события
    """
    if event.event_id not in events:
        events[event.event_id] = event
        return {}

    event_before = deepcopy(events[event.event_id])
    for p_name, p_value in event.model_dump(exclude_unset=True).items():
        setattr(events[event.event_id], p_name, p_value)

    if event.state != event_before.state and event.state in (EventState.FINISHED_WIN, EventState.FINISHED_LOSE):
        data = event.model_dump(mode="json")
        async with AsyncClient(verify=False) as client:
            await client.post(f'{BET_MAKER_API_BASE}/events/action', json=data)

    return {}


@app.get('/event/{event_id}')
async def get_event(event_id: str = Path()):
    """
        Получение события по id
    """
    if event_id in events:
        return events[event_id]

    raise HTTPException(status_code=404, detail="Event not found")


@app.get('/events')
async def get_events() -> list:
    """
        Получение списка событий
    """
    return list(e for e in events.values() if time.time() < e.deadline)
