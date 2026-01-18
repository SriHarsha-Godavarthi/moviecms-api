from datetime import date
from typing import Optional
from sqlalchemy import String, Date, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Movie(Base):
    __tablename__ = "movies"

    movieid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Name: Mapped[str] = mapped_column(String(200))
    Image: Mapped[str] = mapped_column(String(500))
    CDNImage: Mapped[str] = mapped_column(String(500))
    # Use Python type `date` for the annotation and SQLAlchemy `Date` for the column
    ReleaseDate: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
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
    # Publication status, admin-managed
    published: Mapped[bool] = mapped_column(Boolean, default=False)
