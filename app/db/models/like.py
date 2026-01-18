"""MoviesLiked join model mapping user likes to movies.

Field names reflect README's specified casing (e.g., `Id`, `CreatedAt`).
"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class MoviesLiked(Base):
    __tablename__ = "moviesliked"

    Id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    CreatedAt: Mapped[str]
    userid: Mapped[int] = mapped_column(ForeignKey("users.userid"))
    movieid: Mapped[int] = mapped_column(ForeignKey("movies.movieid"))
