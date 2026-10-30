from __future__ import annotations

from dataclasses import dataclass
from os import getenv

from .models import Opportunity


@dataclass(frozen=True)
class TelegramConfig:
    bot_token: str
    chat_id: str

    @classmethod
    def from_environment(cls) -> "TelegramConfig | None":
        token, chat_id = getenv("TELEGRAM_BOT_TOKEN"), getenv("TELEGRAM_CHAT_ID")
        return cls(token, chat_id) if token and chat_id else None


def format_telegram_alert(opportunity: Opportunity) -> str:
    reference = (
        f"€{opportunity.fair_value_eur:.2f}"
        if opportunity.fair_value_eur is not None
        else "unavailable"
    )
    return (
        f"ARCHIVE HUNTER — {opportunity.listing.brand}\n"
        f"{opportunity.listing.title}\n"
        f"Ask €{opportunity.listing.asking_price_eur:.2f} | "
        f"Sold-only reference {reference}"
    )
