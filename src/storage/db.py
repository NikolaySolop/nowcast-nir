"""Database engine, session, and declarative base setup."""

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from config import get_settings


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""


def create_database_engine():
    """Create a SQLAlchemy engine using the configured database URL."""

    settings = get_settings()
    return create_engine(settings.sqlalchemy_database_url, pool_pre_ping=True)


def create_schema() -> None:
    """Create all known tables for local MVP development."""

    from storage import models  # noqa: F401

    engine = create_database_engine()
    Base.metadata.create_all(bind=engine)


SessionLocal = sessionmaker(autocommit=False, autoflush=False)


@contextmanager
def session_scope() -> Iterator[Session]:
    """Provide a transactional database session scope."""

    engine = create_database_engine()
    SessionLocal.configure(bind=engine)
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
