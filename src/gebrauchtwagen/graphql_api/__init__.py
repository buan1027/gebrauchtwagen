"""GraphQL-Schnittstelle fuer Gebrauchtwagen."""

from gebrauchtwagen.graphql_api.graphql_types import Gebrauchtwagen
from gebrauchtwagen.graphql_api.schema import Query, graphql_router

__all__ = ["Gebrauchtwagen", "Query", "graphql_router"]
