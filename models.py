from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from database import Base

class PooCoords(Base):
    __tablename__ = "poocoords"

    id: Mapped[int] = mapped_column(primary_key=True)
    userid: Mapped[int]
    username: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())