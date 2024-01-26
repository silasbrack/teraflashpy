from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    import pydantic_numpy as pnp


class PulseData(BaseModel):
    header: str
    time: pnp.NpNDArrayFp32
    magnitude: pnp.NpNDArrayFp32
