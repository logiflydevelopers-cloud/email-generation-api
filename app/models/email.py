from pydantic import BaseModel, Field

class WriteEmailRequest(BaseModel):
    user_key: str
    topic: str
    tone: str
    language_code: str
    length_words: int = Field(500, alias="length")

class ReplyEmailRequest(BaseModel):
    user_key: str
    body: str
    tone: str
    language_code: str
    length_words: int = Field(500, alias="length")

class ReplyEmailRequest(BaseModel):
    user_key: str
    body: str
    tone: str
    language_code: str
    length_words: int = Field(500, alias="length")


class EmailResponse(BaseModel):
    email: str
