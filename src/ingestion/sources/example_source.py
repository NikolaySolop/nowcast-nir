"""Example data source contract for future ingestion implementations."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class SourcePayload:
    """Raw payload returned by an external source."""

    source_name: str
    collected_at: datetime
    payload: dict[str, Any]


def fetch_example_payload() -> SourcePayload:
    """Return a placeholder payload matching the expected source contract."""

    return SourcePayload(
        source_name="example",
        collected_at=datetime.now(timezone.utc),
        payload={},
    )
