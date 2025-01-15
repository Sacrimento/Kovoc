from collections.abc import Sequence

from pydantic import BaseModel

from .vocabulary_item import VocabularyItemDB


class Quizz(BaseModel):
    answers: Sequence[VocabularyItemDB]
    extra_korean: Sequence[str]
    extra_english: Sequence[str]
