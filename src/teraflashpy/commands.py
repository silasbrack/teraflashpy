from __future__ import annotations

from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, ValidationError, field_validator

from teraflashpy.states.system import SystemState, SystemStatus


class Command(Enum):
    SystemStop = "SYSTEM : STOP"
    "Shuts off the laser and stops the shaker action."
    SystemTellStatus = "SYSTEM : TELL STATUS"
    "Reports the system status"
    SystemMonitor = "SYSTEM : MONITOR %d"
    """%d is a decimal value:
0: reports the actual receiver signal, averaged over 2 ms.
1: reports the automatically generated offset of the TIA in a.u.
5: reports the CPU load of the RT processor in %
6: reports effective delay position in ps and the signal value
15: shuts off the automatic TIA offset control
16: shuts on the automatic TIA offset control
25: switches transfer to \u201asliding\u2018
26: switches transfer to \u201ablock\u2018"""
    SystemTiaFull = "SYSTEM : TIA FULL"
    "Switches TIA to full sensitivity"
    SystemTiaAtn1 = "SYSTEM : TIA ATN1"
    "Switches TIA to medium sensitivity"
    SystemTiaAtn2 = "SYSTEM : TIA ATN2"
    "Switches TIA to smallest sensitivity"
    LaserOff = "LASER : OFF"
    "Switches laser off"
    LaserOn = "LASER : ON"
    "Switches laser on"
    LaserSet = "LASER : SET %f"
    "Sets laser pump current. %f: floating number 0..100"
    AcquisitionBegin = "ACQUISITION : BEGIN %f"
    "Sets start position of pulse acquisition in ps. %f: floating number 0..3000, resolution 0.1"
    AcquisitionRange = "ACQUISITION : RANGE %d"
    """Sets measuring range in ps. %d: decimal number 20..200
May only be set when shaker off (acquisition stopped)."""
    AcquisitionStop = "ACQUISITION : STOP"
    "Stops shaker; may last some seconds, since zero position is searched for."
    AcquisitionStart = "ACQUISITION : START"
    "Starts shaker; may last some seconds, since motion amplitude is to be stabilized."
    AcquisitionAverage = "ACQUISITION : AVERAGE %d"
    "Sets number of averages. %d: decimal number 1..30000"
    AcquisitionResetAvg = "ACQUISITION : RESET AVG"
    "Clears the average accumulator."
    TransmissionSliding = "TRANSMISSION : SLIDING"
    "Switches transfer to \u201asliding\u2018 (only from TF5-xxxx up)"
    TransmissionBlock = "TRANSMISSION : BLOCK"
    "Switches transfer to \u201ablock\u2018 (only from TF5-xxxx up)"


# --------------------------------------- CODES ---------------------------------------


class SystemMonitorCode(Enum):
    ReceiverSignal = 0
    "Reports the actual receiver signal, averaged over 2 ms."
    TiaOffset = 1
    "Reports the automatically generated offset of the TIA in a.u."
    RtProcessorCpuLoad = 5
    "Reports the CPU load of the RT processor in %"
    EffectiveDelayPosition = 6
    "Reports effective delay position in ps and the signal value"
    ShutOffAutomaticOffsetControl = 15
    "Shuts off the automatic TIA offset control"
    ShutOnAutomaticOffsetControl = 16
    "Shuts on the automatic TIA offset control"
    SwitchTransferSliding = 25
    "Switches transfer to \u201asliding\u2018"
    SwitchTransferBlock = 26
    "Switches transfer to \u201ablock\u2018"


# --------------------------------------- INPUTS ---------------------------------------


class SystemMonitorInput(BaseModel):
    code: SystemMonitorCode


class LaserSetInput(BaseModel):
    pump_current: Annotated[float, Field(ge=0, le=100)]


class AcquisitionBeginInput(BaseModel):
    start_position: Annotated[float, Field(ge=0, le=3000)]

    @field_validator("start_position")
    @classmethod
    def check_is_divisible(cls: type[AcquisitionBeginInput], v: float) -> float:
        is_divisible = v % 0.1 == 0
        if not is_divisible:
            msg = "start_position must be divisible by 0.1"
            raise ValidationError(msg)
        return v


class AcquisitionRangeInput(BaseModel):
    measuring_range: Annotated[int, Field(ge=20, le=200)]


class AcquisitionAverageInput(BaseModel):
    num_averages: Annotated[int, Field(ge=1, le=30000)]


class NoInput(BaseModel):
    ...


CommandInput = (
    SystemMonitorInput
    | LaserSetInput
    | AcquisitionBeginInput
    | AcquisitionRangeInput
    | AcquisitionAverageInput
    | NoInput
)


# --------------------------------------- OUTPUTS ---------------------------------------


# OUTPUT_TYPE_MAP = {
#     Command.SystemTellStatus: SystemStatus,
#     Command.SystemMonitor: float,
# }
# OUTPUT_TYPE_MAP = defaultdict(lambda: None, OUTPUT_TYPE_MAP)


class CommandResult(Enum):
    Ok = "OK"
    Error = "ERROR"
    Parameter = "PARAM"


# class CommandOutput(BaseModel):
#     result: CommandResult
#     state: SystemState
#     value: Any

# CommandT = TypeVar("CommandT")


# CommandInput = BaseCommandInput


# class GenericCommand(BaseModel, Generic[CommandT]):
#     command: CommandT
#     command_input: Annotated[CommandInput]


def run(state: SystemState, command: Command, inputs: CommandInput):
    match command:
        case Command.SystemStop:
            # output = run(command, inputs)
            result: CommandResult = CommandResult.Ok
            new_state = state.model_copy(update={"status": SystemStatus.Off}, deep=True)
            value = None
        case Command.SystemTellStatus:
            result: CommandResult = CommandResult.Ok
            new_state = state.model_copy(deep=True)
            value = SystemStatus.On
    match result:
        case CommandResult.Ok:
            return result, new_state, value
        case CommandResult.Error:
            msg = "asdfsafasfda"
            raise Exception(msg)
        case _:
            msg = "CommandResult other than Ok or Error."
            raise ValueError(msg)
        # case Command.SystemMonitor:
        #     return "TEST"
        # case Command.SystemTiaFull:
        #     return state.model_copy(
        #         update={"state": {"laser_state": {"tia_status": TransImpedanceAmplifierStatus.Full}}},
        #         deep=True,
        #     )
        # case Command.SystemTiaAtn1:
        #     return state.model_copy(
        #         update={"state": {"laser_state": {"tia_status": TransImpedanceAmplifierStatus.Medium}}},
        #         deep=True,
        #     )
        # case Command.SystemTiaAtn2:
        #     return state.model_copy(
        #         update={"state": {"laser_state": {"tia_status": TransImpedanceAmplifierStatus.Small}}},
        #         deep=True,
        #     )
        # case Command.LaserOff:
        #     return state.model_copy(update={"state": {"laser_state": {"status": LaserStatus.Off}}}, deep=True)
        # case Command.LaserOn:
        #     return state.model_copy(update={"state": {"laser_state": {"status": LaserStatus.On}}}, deep=True)
        # case Command.LaserSet:
        #     pass
        # case Command.AcquisitionBegin:
        #     pass
        # case Command.AcquisitionRange:
        #     pass
        # case Command.AcquisitionStop:
        #     pass
        # case Command.AcquisitionStart:
        #     pass
        # case Command.AcquisitionAverage:
        #     pass
        # case Command.AcquisitionResetAvg:
        #     pass
        # case Command.TransmissionSliding:
        #     pass
        # case Command.TransmissionBlock:
        #     pass


# message = "\n".join(["CDEF1234", "789AFEDC", "00000002", "????????", u32])
