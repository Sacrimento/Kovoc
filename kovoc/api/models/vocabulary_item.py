from pydantic import NonNegativeInt
from sqlmodel import Field, SQLModel


class VocabularyItem(SQLModel):
    id: int | None = Field(default=None, primary_key=True, exclude=True)
    english: str
    korean: str
    level: NonNegativeInt


class VocabularyItemDB(VocabularyItem, table=True):
    __tablename__ = "vocabulary"
