from pydantic import BaseModel
from typing import Optional, List
from model.User import User

class UserSchema(BaseModel):
    """ Defines data for a new user to be insert
    """
    first_name: str = "Mark"
    last_name: str = "Zuckerberg"
    document: str = "12345678900"

class UserViewSchema(BaseModel):
    """ Defines how a user is represented
    """
    id: int = 1
    first_name: str = "Mark"
    last_name: str = "Zuckerberg"
    balance: float = 0.0
    registration_date : str = "15/09/2023"
    
def reprUser(user:User):
    return {
        "first_name": user.get_first_name(),
        "last_name": user.get_last_name(),
        "document": user.get_document(),
        "balance": user.get_balance(),   
        "registration_date": user.get_registration_date()
    }

class UserSearchSchema(BaseModel):
    """ Defines the structure to search for a user.
        Users are search by their id number
    """
    id: str = 1
    
class UserSumBalanceSchema(BaseModel):
    """ Defines how a user's balance is updated
        Requires a user id and the amount to be added. It allows negative numbers to decrement the balance.
    """
    id: str = 1
    delta: float = 10.53