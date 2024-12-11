import pytest
from httpx import AsyncClient

BET_MAKER_BASE_URL = 'http://localhost:8001'


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_events(anyio_backend):
    async with AsyncClient(base_url=BET_MAKER_BASE_URL) as ac:
        response = await ac.get('/events')

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_create_and_get_bet(anyio_backend):
    new_bet_request = {
        "event_id": "1",
        "amount": 2000
    }

    async with AsyncClient(base_url=BET_MAKER_BASE_URL) as ac:
        create_response = await ac.post('/bet', json=new_bet_request)

    assert create_response.status_code == 200
    new_bet = create_response.json()
    new_bet['amount'] = float(new_bet['amount'])

    async with AsyncClient(base_url=BET_MAKER_BASE_URL) as ac:
        get_response = await ac.get(f'/bet/{new_bet["bet_id"]}')

    assert get_response.status_code == 200
    assert get_response.json() == new_bet


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_all_bets(anyio_backend):
    async with AsyncClient(base_url=BET_MAKER_BASE_URL) as ac:
        response = await ac.get('/bets')

    assert response.status_code == 200
    assert isinstance(response.json(), list)
