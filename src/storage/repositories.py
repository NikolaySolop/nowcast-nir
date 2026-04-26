"""Repository functions for reading and writing domain data."""

from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from storage.models import RawObservation, SourceRun


def create_source_run(
    session: Session,
    *,
    source_name: str,
    status: str = "started",
    message: str | None = None,
) -> SourceRun:
    """Create a source run status row."""

    source_run = SourceRun(
        source_name=source_name,
        status=status,
        message=message,
    )
    session.add(source_run)
    return source_run


def finish_source_run(
    session: Session,
    *,
    source_run: SourceRun,
    status: str,
    message: str | None = None,
) -> SourceRun:
    """Update a source run after completion or failure."""

    source_run.status = status
    source_run.message = message
    source_run.finished_at = datetime.now(timezone.utc)
    session.add(source_run)
    return source_run


def add_raw_observation(
    session: Session,
    *,
    source_name: str,
    observed_at: datetime,
    payload: dict[str, Any],
) -> RawObservation:
    """Create and persist a raw observation payload."""

    observation = RawObservation(
        source_name=source_name,
        observed_at=observed_at,
        payload=payload,
    )
    session.add(observation)
    return observation
