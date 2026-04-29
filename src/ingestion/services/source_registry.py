"""Registry for ingestion source adapters."""

from __future__ import annotations

from ingestion.adapters.tradingview_vix_adapter import TradingViewVixAdapter

SOURCE_REGISTRY = {
    "tradingview_vix": TradingViewVixAdapter,
}


def get_source_adapter(source_type: str, *, timeout_seconds: int = 30):
    """Instantiate and return an adapter class for configured source type."""

    adapter_cls = SOURCE_REGISTRY[source_type]
    return adapter_cls(timeout_seconds=timeout_seconds)
