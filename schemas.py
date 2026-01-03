from pydantic import BaseModel
from datetime import datetime

class PooCoordsAddSchema(BaseModel):
    userid: int
    username: str
    latitude: float
    longitude: float

class PooCoordsSchema(PooCoordsAddSchema):
    id: int
    created_at: datetime