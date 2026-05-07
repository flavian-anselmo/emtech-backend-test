from sqlalchemy.orm import relationship
from app.database.database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy import Column,ForeignKey,Integer,String,Float,TIMESTAMP


class Customers(Base):
    '''
    customer records 
    '''
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True, nullable=False)
    customer_name = Column(String, nullable=False)
    phone_no = Column(String, nullable=False)
    password = Column(String, nullable = False)



