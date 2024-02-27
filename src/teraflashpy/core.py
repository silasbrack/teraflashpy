from __future__ import annotations

from enum import Enum

from pydantic import BaseModel

LOCALHOST = "127.0.0.1"


class AcquisitionMode(Enum):
    Synchronous = 0
    Asynchronous = 1


ACQUISITION_PORT_MAP = {
    AcquisitionMode.Synchronous: 6007,
    AcquisitionMode.Asynchronous: 6006,
}


class Config(BaseModel):
    acquisition_mode: AcquisitionMode = AcquisitionMode.Synchronous
