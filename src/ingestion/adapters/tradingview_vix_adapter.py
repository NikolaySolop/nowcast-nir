"""TradingView adapter for ingesting TVC:VIX candles at 15-minute frequency."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import httpx

TRADINGVIEW_HISTORY_URL = "https://tvc4.investing.com/history"
TRADINGVIEW_SYMBOL = "TVC:VIX"
TRADINGVIEW_SOURCE_CODE = "TRADINGVIEW"
DEFAULT_RESOLUTION = "15"


@dataclass(frozen=True)
class VixCandle:
    """Normalized VIX candle from TradingView history endpoint."""

    observed_at: datetime
    open_value: Decimal
    high_value: Decimal
    low_value: Decimal
    close_value: Decimal


class TradingViewVixAdapter:
    """Fetch VIX candle history with browser-like headers."""

    def __init__(self, timeout_seconds: int = 30) -> None:
        self.timeout_seconds = timeout_seconds

    def fetch_candles(
        self,
        *,
        start_at: datetime | None,
        end_at: datetime | None = None,
        resolution: str = DEFAULT_RESOLUTION,
    ) -> list[VixCandle]:
        """Fetch VIX candles from TradingView history endpoint."""

        now = datetime.now(UTC)
        to_dt = (end_at or now).astimezone(UTC)
        from_dt = (start_at or (to_dt - timedelta(days=5))).astimezone(UTC)

        params = {
            "symbol": TRADINGVIEW_SYMBOL,
            "resolution": resolution,
            "from": int(from_dt.timestamp()),
            "to": int(to_dt.timestamp()),
        }

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json,text/plain,*/*",
            "Origin": "https://www.tradingview.com",
            "Referer": "https://www.tradingview.com/symbols/TVC-VIX/",
        }

        with httpx.Client(timeout=self.timeout_seconds, headers=headers) as client:
            response = client.get(TRADINGVIEW_HISTORY_URL, params=params)
            response.raise_for_status()
            payload = response.json()

        if payload.get("s") != "ok":
            return []

        candles: list[VixCandle] = []
        for timestamp, open_value, high_value, low_value, close_value in zip(
            payload.get("t", []),
            payload.get("o", []),
            payload.get("h", []),
            payload.get("l", []),
            payload.get("c", []),
            strict=True,
        ):
            observed_at = datetime.fromtimestamp(timestamp, tz=UTC)
            candles.append(
                VixCandle(
                    observed_at=observed_at,
                    open_value=Decimal(str(open_value)),
                    high_value=Decimal(str(high_value)),
                    low_value=Decimal(str(low_value)),
                    close_value=Decimal(str(close_value)),
                ),
            )

        if start_at is None:
            return candles

        start_at_utc = start_at.astimezone(UTC)
        return [candle for candle in candles if candle.observed_at > start_at_utc]
