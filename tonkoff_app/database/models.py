from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, Float, Text, DateTime, BigInteger

Base = declarative_base()

class Profile(Base):
    __tablename__ = "profile"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_username: Mapped[str] = mapped_column(String(32), nullable=True)
    wallet_address: Mapped[str] = mapped_column(String(), nullable=True)
    ref_link: Mapped[str] = mapped_column(String(), nullable=True)
    count_invited: Mapped[int] = mapped_column(Integer, default=0)
    payload: Mapped[int] = mapped_column(Integer, nullable=True)
    balance: Mapped[int] = mapped_column(Integer, default=0)
    friends_balance: Mapped[int] = mapped_column(Integer, default=0)
    user_score: Mapped[int] = mapped_column(Integer, default=0)
    friends_score: Mapped[int] = mapped_column(Integer, default=0)
    total: Mapped[float] = mapped_column(Float(asdecimal=True), default=0)
    last_reset_time: Mapped[DateTime] = mapped_column(DateTime, nullable=True)