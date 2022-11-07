from datetime import datetime
from sqlalchemy import Column, Float, ForeignKey, Text, DateTime, Integer
from account.models import Account


from db import Base


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now)
    shipping_address = Column(Text)
    user_id = Column(Integer, ForeignKey(Account.id, ondelete="CASCADE"))


