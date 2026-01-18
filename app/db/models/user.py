"""User model per README spec.

Fields follow the frontend naming specified in the README to ensure
payload and response compatibility (e.g., `isPremiumUser`, `userid`).
"""

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    userid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    firstname: Mapped[str] = mapped_column(String(100))
    lastname: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    phonenumber: Mapped[str] = mapped_column(String(30))
    isPremiumUser: Mapped[bool] = mapped_column(Boolean, default=False)
