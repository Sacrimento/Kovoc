from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import select

from kovoc.api.models import (
    Page,
    Pagination,
    VocabularyItem,
    VocabularyItemDB,
    paginate,
)
from kovoc.utils import pg_session

router = APIRouter(prefix="/vocabulary", tags=["vocabulary"])


@router.get("")
async def get_vocabulary(pagination: Pagination) -> Page[VocabularyItemDB]:
    with pg_session() as session:
        statement = (
            select(VocabularyItemDB)
            .offset((pagination.page - 1) * pagination.limit)
            .limit(pagination.limit)
        )
        vocab = session.exec(statement).all()

        total = session.exec(func.count(VocabularyItemDB.id)).scalar()  # type: ignore[arg-type, call-overload]

    return paginate(vocab, total, pagination.page, pagination.limit)


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
