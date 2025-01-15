from collections.abc import Sequence

from fastapi import APIRouter
from pydantic import NonNegativeInt
from sqlalchemy import func
from sqlmodel import select

from kovoc.api.models import Quizz, VocabularyItemDB
from kovoc.utils import pg_session

router = APIRouter(prefix="/quizz", tags=["quizz"])


@router.get("")
async def get_quizz(
    level_eq: NonNegativeInt = 0,
    level_lt: NonNegativeInt = 0,
    nb_items: NonNegativeInt = 5,
    extra: bool = False,
) -> Quizz:
    with pg_session() as session:
        statement = select(VocabularyItemDB)
        if level_eq:
            statement = statement.where(VocabularyItemDB.level == level_eq)
        elif level_lt:
            statement = statement.where(VocabularyItemDB.level < level_lt)

        filtered_vocab = statement

        statement = statement.order_by(func.random()).limit(nb_items)
        answers = session.exec(statement).all()

        extra_words: Sequence[VocabularyItemDB] = []
        if extra:
            statement = filtered_vocab.filter(
                VocabularyItemDB.id.not_in([v.id for v in answers])  # type: ignore[union-attr]
            )
            statement = statement.order_by(func.random()).limit(nb_items * 2)
            extra_words = session.exec(statement).all()

    return Quizz(
        answers=answers,
        extra_korean=[v.korean for v in extra_words],
        extra_english=[v.english for v in extra_words],
    )
