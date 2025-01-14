from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from kovoc.api.models import VocabularyItem
from kovoc.utils import pg_session

router = APIRouter(prefix="/vocabulary", tags=["vocabulary"])


@router.get("")
async def get_vocabulary(
    english: str | None = None, korean: str | None = None
) -> VocabularyItem:
    if not (english or korean):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least korean or english query parameter is required",
        )

    with pg_session() as session:
        statement = select(VocabularyItem)
        if english:
            statement = statement.where(VocabularyItem.english == english)
        if korean:
            statement = statement.where(VocabularyItem.korean == korean)
        vocab = session.exec(statement).first()

    if not vocab:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No vocabulary item found for specified parameters",
        )

    return vocab
