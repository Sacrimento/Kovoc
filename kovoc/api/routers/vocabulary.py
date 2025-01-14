from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound
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


# TODO: with privileges
@router.post("")
async def post_vocabulary(vocabulary: VocabularyItem) -> VocabularyItem:
    with pg_session() as session:
        session.add(vocabulary)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            statement = (
                select(VocabularyItem)
                .where(VocabularyItem.english == vocabulary.english)
                .where(VocabularyItem.korean == vocabulary.korean)
            )
            return session.exec(statement).one()

    return vocabulary


# TODO: with privileges
@router.delete("/{id}")
async def delete_vocabulary(vocab_id: int) -> VocabularyItem:
    with pg_session() as session:
        statement = select(VocabularyItem).where(VocabularyItem.id == vocab_id)
        try:
            vocab = session.exec(statement).one()
        except NoResultFound as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No vocabulary item with id={vocab_id}",
            ) from exc

        session.delete(vocab)
        session.commit()

    return vocab
