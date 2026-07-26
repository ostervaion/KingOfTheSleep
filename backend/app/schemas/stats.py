from pydantic import BaseModel


class TodayStatsRead(BaseModel):

    wins: int
    losses: int
