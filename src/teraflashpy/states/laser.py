from __future__ import annotations

from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, ValidationError, field_validator

# if TYPE_CHECKING:
from teraflashpy.states.trans_impedance_amplifier import TransImpedanceAmplifierStatus
from teraflashpy.states.transfer import TransferStatus


class LaserStatus(Enum):
    Off = 0
    On = 1


class AcquisitionStatus(Enum):
    Off = 0
    On = 1


class AcquisitionState(BaseModel):
    state: AcquisitionStatus
    start_position: Annotated[float, Field(ge=0, le=3000)]
    measuring_range: Annotated[int, Field(ge=20, le=200)]
    num_averages: Annotated[int, Field(ge=1, le=30000)]

    @field_validator("start_position")
    @classmethod
    def check_is_divisible(cls: type[AcquisitionState], v: float) -> float:
        is_divisible = v % 0.1 == 0
        if not is_divisible:
            msg = "start_position must be divisible by 0.1"
            raise ValidationError(msg)
        return v


class LaserState(BaseModel):
    status: LaserStatus
    pump_current: Annotated[int, Field(ge=0, le=100)]
    transfer_status: TransferStatus
    tia_status: TransImpedanceAmplifierStatus
    # acquisition_state: AcquisitionState
