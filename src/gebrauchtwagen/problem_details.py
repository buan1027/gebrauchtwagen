"""Problem Details fuer konsistente API-Fehlerantworten."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from fastapi import Response
from fastapi.responses import JSONResponse

__all__ = ["create_problem_details"]

NOT_FOUND = 404
UNPROCESSABLE_CONTENT = 422

type ProblemDetail = Any


@dataclass(eq=False, slots=True, kw_only=True)
class ProblemDetails:
    """Datenstruktur fuer konsistente API-Fehlerantworten."""

    title: str
    status_code: int
    detail: ProblemDetail = None


def create_problem_details(
    status_code: int,
    detail: ProblemDetail = None,
) -> Response:
    """Erzeuge eine Problem-Details-Antwort fuer Client-Fehler."""
    match status_code:
        case 404:
            problem_details = ProblemDetails(
                title="Not Found",
                status_code=status_code,
                detail=detail,
            )
        case 422:
            problem_details = ProblemDetails(
                title="Unprocessable Content",
                status_code=status_code,
                detail=detail,
            )
        case _:
            problem_details = ProblemDetails(
                title="Client Error",
                status_code=status_code,
                detail=detail,
            )
    return JSONResponse(
        status_code=status_code,
        content=asdict(problem_details),
        media_type="application/problem+json",
    )
