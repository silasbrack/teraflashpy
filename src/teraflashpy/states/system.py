from enum import Enum

from pydantic import BaseModel

from teraflashpy.states.laser import LaserState


class SystemStatus(Enum):
    Off = 0
    On = 1


class SystemState(BaseModel):
    status: SystemStatus
    laser_state: LaserState
