import sqlalchemy

from baza import Base


class User(Base):
    __tablename__ = "users"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    tg_user_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True)
    sm_penis = sqlalchemy.Column(sqlalchemy.BigInteger)
