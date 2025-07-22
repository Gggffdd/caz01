from sqlalchemy import create_engine, Column, Integer, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    balance = Column(Integer, default=1000)

def init_db():
    engine = create_engine(os.getenv("DATABASE_URL"))
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

Session = init_db()

def get_user_balance(user_id):
    with Session() as session:
        user = session.get(User, user_id)
        return user.balance if user else None

def update_user_balance(user_id, amount, increment=False):
    with Session() as session:
        user = session.get(User, user_id)
        
        if not user:
            user = User(id=user_id, balance=amount)
            session.add(user)
        else:
            if increment:
                user.balance += amount
            else:
                user.balance = amount
        
        session.commit()
