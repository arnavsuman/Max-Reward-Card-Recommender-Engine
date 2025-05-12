from pydantic import BaseModel

class UserProfile(BaseModel):
    name: str
    email: str
    preferences: dict
    statements: list
