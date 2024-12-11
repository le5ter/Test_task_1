from contextlib import asynccontextmanager
from fastapi import FastAPI, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from models import Bet, Event, EventState, BetStatus
from postgres.client import PGManager
from postgres.models import BetPg
from settings import LINE_PROVIDER_API_BASE


@asynccontextmanager
async def lifespan(app: FastAPI): # noqa
    await postgres.client.init_tables()
    yield

app = FastAPI(lifespan=lifespan)
postgres = PGManager()


@app.get('/events')
async def get_events() -> list:
    """
        Получение списка событий
    """
    async with AsyncClient(verify=False) as client:
        response = await client.get(f'{LINE_PROVIDER_API_BASE}/events')

        return response.json()


@app.post('/events/action')
async def on_event_action(event: Event) -> None:
    """
        Callback url для обновления статуса ставок если статус события изменился
    """
    if event.state not in (EventState.FINISHED_WIN, EventState.FINISHED_LOSE):
        return

    mapper = {
        EventState.FINISHED_WIN: BetStatus.FINISHED_WIN,
        EventState.FINISHED_LOSE: BetStatus.FINISHED_LOSE
    }

    async with postgres.client() as session:
        session: AsyncSession
        bets_for_event = (await session.execute(
           select(BetPg)
            .filter_by(event_id=event.event_id,
                       status=BetStatus.IN_PROGRESS)
        )).scalars().all()

        if bets_for_event:
            for bet in bets_for_event:
                bet.status = mapper[event.state]

        await session.commit()



@app.post('/bet')
async def create_bet(bet: Bet) -> dict:
    """
        Совершение ставки на событие
    """
    new_bet = BetPg(**bet.model_dump(by_alias=True))

    async with postgres.client() as session:
        session.add(new_bet)
        await session.commit()

    return bet.model_dump()


@app.get('/bets')
async def get_bets() -> list:
    """
        Получение списка ставок
    """
    result = []
    async with postgres.client() as session:
        session: AsyncSession
        bets = (await session.execute(
            select(BetPg)
        )).scalars().all()

        for bet in bets:
            serialized = bet.to_dict()
            result.append(serialized)

    return result


@app.get('/bet/{bet_id}')
async def get_bet(bet_id: str = Path()) -> dict:
    """
        Получение ставки по id
    """
    async with postgres.client() as session:
        session: AsyncSession
        bet = (await session.execute(
            select(BetPg)
            .filter_by(id=bet_id)
        )).scalar_one_or_none()

        if bet:
            return bet.to_dict()

    return {}
