from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

class User(Base):
    
    __tablename__ = 'users'
    
    id = Column("id", Integer, primary_key = True) 
    first_name = Column(String(100))
    last_name = Column(String(100))
    document = Column(String(11))
    
    balance = Column(Float, default = 0.0)
    registration_date =  Column(DateTime, default = datetime.now())

    
    def __init__(self, first_name:str, last_name:str, document:str):
        
        self.first_name = first_name
        self.last_name = last_name
        self.document = document
            
        self.balance = 0.0    
        self.registration_date = datetime.now()
    
    def get_first_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name
    
    def get_full_name(self):
        return f"'{self.last_name.upper()}, {self.first_name.capitalize()}'"
    
    def get_balance(self):
        return self.balance
    
    def get_document(self):
        return self.document
    
    def set_balance(self, value: float):
        self._balance = value
            
    def get_registration_date(self):
        return self.registration_date

        
        