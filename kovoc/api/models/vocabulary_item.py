from sqlmodel import Field, SQLModel


class VocabularyItem(SQLModel, table=True):
    __tablename__ = "vocabulary"

    id: int | None = Field(default=None, primary_key=True, exclude=True)
    english: str
    korean: str
