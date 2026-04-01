"""Grundkonfiguration für SQLAlchemy."""

from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker

from gebrauchtwagen.config.settings import load_settings

settings = load_settings()

db_url = URL.create(
    drivername="postgresql+psycopg",
    username=settings.db.username,
    password=settings.db.password,
    host=settings.db.host,
    port=settings.db.port,
    database=settings.db.name,
)

engine = create_engine(
    db_url,
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


def check_database_connection() -> None:
    """Prüfe, ob die Anwendung die Datenbank erreichen kann."""
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
