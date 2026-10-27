
from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
    project: str | None = None
    speaker: str | None = None
    date_from: str | None = None
    date_to: str | None = None
    as_of: str | None = None
