from sqlmodel import Session, create_engine

from .settings import get_settings


def pg_session() -> Session:
    settings = get_settings()
    engine = create_engine(
        f"postgresql://{settings.pg_user}:{settings.pg_pass}@localhost/{settings.pg_db}"
    )

    return Session(engine)
