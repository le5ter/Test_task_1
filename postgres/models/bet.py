from sqlalchemy import String, Enum, Numeric
from sqlalchemy.orm import mapped_column

from postgres.base import Base
from models.bet import BetStatus


class BetPg(Base):
    # BetPg = BetPostgres
    __tablename__ = 'bets'

    id = mapped_column(String(32), primary_key=True)
    event_id = mapped_column(String(32), nullable=False)
    status = mapped_column(Enum(BetStatus, name="bet_statuses"), nullable=False)
    amount = mapped_column(Numeric, nullable=False)

    alias = {
        "id": "bet_id"
    }
