# app/schemas/protocol_impact.py
from pydantic import BaseModel


class ProtocolImpactRead(BaseModel):
    """
    DTO for the Protocol Impact widget.
    Not tied to any single table — computed by combining
    UserProtocol (usage dates) + ScoreHistory (sleep scores).
    """
    id: int          # protocol_id
    name: str        # protocol name
    percentage: float  # % impact vs baseline, computed server-side
    daysUsed: int      # count of days this protocol was used