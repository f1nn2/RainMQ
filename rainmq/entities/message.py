from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Message:
    id: str

    producer_url: str
    http_method: str

    headers: Optional[dict]
    query_str: Optional[str]
    json: Optional[dict]

    inserted_at: datetime
