from datetime import datetime

from pydantic import BaseModel, HttpUrl


class KbButtonSchema(BaseModel):
    name: str
    url: HttpUrl


class UserSchema(BaseModel):
    id: int
    full_name: str
    created_at: datetime
