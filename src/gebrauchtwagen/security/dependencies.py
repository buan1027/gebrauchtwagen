"""Factory-Funktionen fuer Security-Dependencies."""

from gebrauchtwagen.security.token_service import TokenService

__all__ = ["get_token_service"]

_token_service = TokenService()


def get_token_service() -> TokenService:
    """Liefere den Token-Service als Singleton."""
    return _token_service
