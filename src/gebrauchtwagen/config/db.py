"""Grundkonfiguration für SQLAlchemy."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from gebrauchtwagen.config.settings import load_settings

settings = load_settings()

engine = create_engine(
    settings.db.url,
    echo=settings.db.echo,
)

SessionFactory = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    autocommit=False,
)


def get_session() -> Session:
    """Erzeuge eine Datenbank-Session."""
    return SessionFactory()
