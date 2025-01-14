from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import select

from kovoc.api.models import VocabularyItem, VocabularyItemDB
from kovoc.utils import pg_session

router = APIRouter(prefix="/vocabulary", tags=["vocabulary"])


@router.get("")
async def get_vocabulary(
    english: str | None = None, korean: str | None = None
) -> VocabularyItemDB:
    if not (english or korean):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least korean or english query parameter is required",
        )

    with pg_session() as session:
        statement = select(VocabularyItemDB)
        if english:
            statement = statement.where(VocabularyItemDB.english == english)
        if korean:
            statement = statement.where(VocabularyItemDB.korean == korean)
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
                select(VocabularyItemDB)
                .where(VocabularyItemDB.english == vocabulary.english)
                .where(VocabularyItemDB.korean == vocabulary.korean)
            )
            return session.exec(statement).one()

    return vocabulary


# TODO: with privileges
@router.delete("/{id}")
async def delete_vocabulary(vocab_id: int) -> VocabularyItemDB:
    with pg_session() as session:
        statement = select(VocabularyItemDB).where(VocabularyItemDB.id == vocab_id)
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
