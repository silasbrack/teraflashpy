from __future__ import annotations

from datetime import datetime  # noqa: TCH003

import pydantic_numpy as pnp  # noqa: TCH002
from pydantic import BaseModel


class PulseData(BaseModel):
    timestamp: datetime
    header: list[str]
    time: pnp.NpNDArrayFp32
    magnitude: pnp.NpNDArrayFp32
