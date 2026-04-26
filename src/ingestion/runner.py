"""Entry point for scheduled or manual data ingestion runs."""

import json

from config import get_settings
from storage.db import create_schema


def run_ingestion() -> dict[str, str]:
    """Run all configured ingestion sources.

    This is a placeholder. The first real implementation should call one source,
    validate the payload, and persist raw plus normalized data through storage.
    """

    settings = get_settings()
    if settings.auto_create_tables:
        create_schema()

    return {
        "status": "skipped",
        "reason": "no ingestion sources are implemented yet",
    }


def main() -> None:
    """CLI entry point for the ingestion worker."""

    print(json.dumps(run_ingestion(), indent=2))


if __name__ == "__main__":
    main()
