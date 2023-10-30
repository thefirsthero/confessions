from pydantic import BaseModel

# class User(BaseModel):
#     id: str
#     name: str
#     lastName: str
#     birthYear: int 

class Confession(BaseModel):
    id: int
    confession: str
    location: str