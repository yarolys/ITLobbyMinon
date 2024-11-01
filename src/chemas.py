from pydantic import BaseModel, HttpUrl


class KbButton(BaseModel):
    name: str
    url: HttpUrl
