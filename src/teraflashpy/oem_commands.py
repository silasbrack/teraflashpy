from enum import Enum

from pydantic import BaseModel


class RcCommand(Enum):
    LaserOff = "RC-LASER : OFF"
    "Switch off laser and emitter voltage"
    LaserOn = "RC-LASER : ON"
    "Switch on laser and emitter voltage"
    VoltageOff = "RC-VOLTAGE : OFF"
    "Switch off emitter voltage"
    VoltageOn = "RC-VOLTAGE : ON"
    "Switch on emitter voltage; works only, if laser is already on"
    RunOff = "RC-RUN : OFF"
    "Stop measurement"
    RunOn = "RC-RUN : ON"
    "Start measurement"
    Begin = "RC-BEGIN %.1f"
    "Set start point in ps"
    Range = "RC-RANGE %d measuring range in ps"
    "Set measuring range in ps"
    Average = "RC-AVERAGE %d averaging number"
    "Set averaging number"
    TransferSliding = "RC-TRANSFER : SLIDING"
    "Set data transfer to: continuously"
    TransferBlock = "RC-TRANSFER : BLOCK"
    "Set data transfer to: not until complete averaging"
    AnalysisReduced = "RC-ANALYSIS : REDUCED"
    "Set data analysis to: block by block"
    AnalysisFullRate = "RC-ANALYSIS : FULL RATE"
    "Set data analysis to: full rate"
    TiaIntern = "RC-TIA : INTERN"
    "Set measurement to: internal TIA"
    TiaExtern = "RC-TIA : EXTERN"
    "Set measurement to: external TIA"
    TiaSensitivity = "RC-TIA : SENSITIVITY %d  measuring range in nA"
    "Set TIA measuring range (100, 300, 1000 [nA +/-])"
    V22RcFilePath = "V 22RC-FILEPATH %s path string"
    "Set file path for saving pulse data"
    WaitOn = "RC-WAIT : ON"
    "Switch on WAIT state"
    WaitOff = "RC-WAIT : OFF"
    "Switch off WAIT state"
    AutoOn = "RC-AUTO : ON"
    "Switch on AUTO-WAIT"
    AutoOff = "RC-AUTO : OFF"
    "Switch off AUTO-WAIT"
    SaveWithSpectrum = "RC-SAVE W-S"
    "Save pulse data with spectrum"
    SaveWithoutSpectrum = "RC-SAVE WO-S"
    "Save pulse data without spectrum"
    ReverseOn = "RC-REVERSE : ON"
    "Switch on REVERSE mode"
    ReverseOff = "RC-REVERSE : OFF"
    "Switch off REVERSE mode"
    SetRef = "RC-REF"
    "Set current measurement as Reference"
    DeleteRef = "RC-CLR"
    "Delete a present Reference, re-normalize frequency spectra"
    SetBackground = "RC-BGR"
    "Set current measurement as Background"
    DeleteBackground = "RC-BCL"
    "Delete a present Background"


class BeginInput(BaseModel):
    start_point: float
    "Start point in ps"


class RangeInput(BaseModel):
    measuring_range: int
    "Measuring range in ps"


class AverageInput(BaseModel):
    averaging_number: int
    "Averaging number"


class TiaSensitivityInput(BaseModel):
    measuring_range = int
    "TIA measuring range (100, 300, 1000 [nA +/-])"


class V22RcFilePathInput(BaseModel):
    file_path: str
    "File path for saving pulse data"


class RdCommand(Enum):
    Amplitude = "RD-AMPLITUDE"
    "Read amplitude [nA]"
    TotalAcquisitionTime = "RD-TAC.TIME"
    "Read total acquisition time [s]"
    RelativeAcquisitionTime = "RD-XAC.TIME"
    "Read relative acquisition time"
    LaserState = "RD-LASER"
    "Read laser state"
    EmmitterSupplyState = "RD-VOLTAGE"
    "Read emitter supply state"
    AcquisitionState = "RD-RUN"
    "Read acquisition state"
    MeasuringStartPoint = "RD-BEGIN"
    "Read measuring start point [ps]"
    MeasuringRange = "V 22RD-RANGE"
    "Read measuring range [ps]"
    DesiredAverage = "RD-AVERAGE"
    "Read desired average"
    TransferMode = "RD-TRANSFER"
    "Read transfer mode"
    AnalysisMode = "RD-ANALYSIS"
    "Read analysis mode"
    TiaMode = "RD-TIA-MODE"
    "Read TIA mode"
    TiaSensitivity = "RD-TIA-SENSITIVITY"
    "Read TIA sensitivity"
    WaitButtonState = "RD-WAIT"
    "Read WAIT button state"
    AutoButtonState = "RD-AUTO"
    "Read auto button state"
    ReverseButtonState = "RD-REVERSE"
    "Read REVERSE button state"


OemCommand = RcCommand | RdCommand


class OemCommandOutput(Enum):
    Ok = "OK"
    Error = "ERROR"
