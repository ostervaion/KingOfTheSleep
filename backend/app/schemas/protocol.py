from pydantic import BaseModel
from datetime import datetime
from sqlmodel import SQLModel
 



class ProtocolImpactRead(BaseModel):

    id: int          # protocol_id
    name: str        # protocol name
    percentage: float  # % impact vs baseline, computed server-side
    daysUsed: int      # count of days this protocol was used


    
class RankedProtocolData(BaseModel):

    ranking: int
    protocol: str
    usage: int  
    winrate: float

class RankedProtocolsRead(BaseModel):

    winner_protocols: list[RankedProtocolData]
    loser_protocols: list[RankedProtocolData]

class ProtocolSelection(SQLModel):
    protocol_ids: list[int]
 
 
class UserProtocolPublic(SQLModel):
    id: int
    user_id: int
    protocol_id: int
    created_at: datetime
