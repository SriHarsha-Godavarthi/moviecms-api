"""Pydantic schemas for the MoviesLiked join table.

- `LikeCreate`: input payload linking a user and a movie
- `LikeRead`: output model including `Id` and `CreatedAt`
"""

from pydantic import BaseModel

class LikeBase(BaseModel):
    """Shared fields indicating the user and movie identifiers."""
    userid: int
    movieid: int

class LikeCreate(LikeBase):
    """Input model for creating a like entry."""
    pass

class LikeRead(LikeBase):
    """Response model including server-generated `Id` and timestamp `CreatedAt`."""
    Id: int
    CreatedAt: str

    class Config:
        from_attributes = True
