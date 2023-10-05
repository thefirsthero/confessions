from pydantic import BaseModel

# class User(BaseModel):
#     id: str
#     name: str
#     lastName: str
#     birthYear: int 

class Confession(BaseModel):
    id: str
    confession: str
    location: str