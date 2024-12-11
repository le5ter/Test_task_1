import enum
import uuid
from decimal import Decimal, ROUND_HALF_UP
from pydantic import BaseModel, Field, model_validator


def generate_bet_id():
    return uuid.uuid4().hex


class BetStatus(enum.Enum):
    IN_PROGRESS = "in_progress"
    FINISHED_WIN = "win"
    FINISHED_LOSE = "lose"


class Bet(BaseModel):
    bet_id: str = Field(default_factory=generate_bet_id, alias="id")
    event_id: str
    status: BetStatus = BetStatus.IN_PROGRESS
    amount: Decimal

    @model_validator(mode="after")
    def round_decimal(self):
        self.amount = self.amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        return self
