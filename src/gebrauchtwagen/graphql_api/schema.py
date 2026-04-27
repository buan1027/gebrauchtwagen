"""Schema fuer GraphQL durch Strawberry."""

from __future__ import annotations

from typing import Final

import strawberry
from strawberry.fastapi import GraphQLRouter

from gebrauchtwagen.graphql_api.graphql_types import Gebrauchtwagen
from gebrauchtwagen.service import gebrauchtwagen_service

__all__ = ["Query", "graphql_router"]


@strawberry.type
class Query:
    """Queries, um Gebrauchtwagen zu lesen."""

    @strawberry.field
    def gebrauchtwagen(self) -> list[Gebrauchtwagen]:
        """Liefere alle Gebrauchtwagen aus der PostgreSQL-Persistenz."""
        return [
            Gebrauchtwagen.from_dto(dto)
            for dto in gebrauchtwagen_service.list_gebrauchtwagen()
        ]


schema: Final = strawberry.Schema(query=Query)
graphql_router: Final = GraphQLRouter(schema)
