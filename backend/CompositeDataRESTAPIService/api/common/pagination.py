import math
from dataclasses import dataclass

from api.db.base import db


@dataclass
class Pagination:
    items: list
    total: int
    pages: int
    page: int
    has_next: bool
    has_prev: bool


def paginate(query, page, per_page) -> Pagination:
    offset = (page - 1) * per_page

    count_stmt = db.select(db.func.count()).select_from(query.subquery())
    total_count = db.session.execute(count_stmt).scalar()
    total_pages = math.ceil(total_count / per_page) if total_count > 0 else 0

    items = db.session.execute(
        query.limit(per_page).offset(offset)
    )

    return Pagination(
        items=items,
        total=total_count,
        page=page,
        pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )




