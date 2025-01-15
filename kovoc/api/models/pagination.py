from collections.abc import Sequence
from typing import Annotated, Generic, TypeVar

from fastapi import Depends
from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt

from kovoc.utils.settings import get_settings

T = TypeVar("T", bound=BaseModel)

settings = get_settings()


class Page(BaseModel, Generic[T]):
    total: NonNegativeInt
    page: PositiveInt
    limit: PositiveInt = Field(ge=1, le=settings.max_page_size)
    items: Sequence[T]

    @classmethod
    def create(cls, items: Sequence[T], total: int, page: int, limit: int) -> "Page[T]":
        return cls(
            items=items,
            total=total,
            page=page,
            limit=limit,
        )


def paginate(
    items: Sequence[T],
    total: int,
    page: int,
    limit: int,
) -> Page[T]:
    """
    Wraps a model into a well-formated API page.

    Parameters:
    - `items`: the objects to return
    - `total`: the total number of objects without pagination that match the request
    - `page`
    - `limit`
    """

    return Page.create(
        items=items,
        total=total,
        page=page,
        limit=limit,
    )


class RequestPage(BaseModel):
    page: PositiveInt
    limit: PositiveInt = Field(ge=1, le=settings.max_page_size)


def request_page(page: int = 1, limit: int = settings.max_page_size) -> RequestPage:
    page = max(page, 1)
    limit = max(min(limit, settings.max_page_size), 1)
    return RequestPage(page=page, limit=limit)


Pagination = Annotated[RequestPage, Depends(request_page)]
