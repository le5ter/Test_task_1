import enum
from typing import Optional
from decimal import Decimal, ROUND_HALF_UP
from pydantic import BaseModel, model_validator


class EventState(enum.Enum):
    NEW = "new"
    FINISHED_WIN = "finished_win"
    FINISHED_LOSE = "finished_lose"


class Event(BaseModel):
    event_id: str
    coefficient: Optional[Decimal] = None
    deadline: Optional[int] = None
    state: Optional[EventState] = None

    @model_validator(mode="after")
    def round_decimal(self):
        if self.coefficient:
            self.coefficient = self.coefficient.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        return self
