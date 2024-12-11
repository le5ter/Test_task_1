import time
import pytest
from httpx import AsyncClient

from models import EventState

LINE_PROVIDER_BASE_URL = 'http://localhost:8000'


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_simple_workflow(anyio_backend):
    test_id = 'test_id'

    test_event = {
        'event_id': test_id,
        'coefficient': "1.00",
        'deadline': int(time.time()) + 600,
        'state': EventState.NEW.value
    }

    async with AsyncClient(base_url=LINE_PROVIDER_BASE_URL) as ac:
        create_response = await ac.put('/event', json=test_event)

    assert create_response.status_code == 200

    async with AsyncClient(base_url=LINE_PROVIDER_BASE_URL) as ac:
        response = await ac.get(f'/event/{test_id}')

    assert response.status_code == 200
    assert response.json() == test_event

    updated_event = test_event.copy()
    updated_event['state'] = EventState.FINISHED_WIN.value

    async with AsyncClient(base_url=LINE_PROVIDER_BASE_URL) as ac:
        update_response = await ac.put('/event', json={'event_id': test_id, 'state': EventState.FINISHED_WIN.value})

    assert update_response.status_code == 200

    async with AsyncClient(base_url=LINE_PROVIDER_BASE_URL) as ac:
        response = await ac.get(f'/event/{test_id}')

    assert response.status_code == 200
    assert response.json() == updated_event
