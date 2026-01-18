from typing import Optional
from sqlalchemy import String, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Movie(Base):
    __tablename__ = "movies"

    movieid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Name: Mapped[str] = mapped_column(String(200))
    Image: Mapped[str] = mapped_column(String(500))
    CDNImage: Mapped[str] = mapped_column(String(500))
    ReleaseDate: Mapped[Optional[Date]] = mapped_column(nullable=True)
    ActorsList: Mapped[str] = mapped_column(String(500))
    language: Mapped[str] = mapped_column(String(50))
    duration: Mapped[int] = mapped_column(Integer)
    CDN_VIDEO: Mapped[str] = mapped_column(String(500))
    description: Mapped[str] = mapped_column(String(1000))
    createdby: Mapped[str] = mapped_column(String(255))
    lastupdated: Mapped[str] = mapped_column(String(50))
    lastupdatedby: Mapped[str] = mapped_column(String(255))
    genre: Mapped[str] = mapped_column(String(100))
    directedby: Mapped[str] = mapped_column(String(255))
    certificatetype: Mapped[str] = mapped_column(String(50))
