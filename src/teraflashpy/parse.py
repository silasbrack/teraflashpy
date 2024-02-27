from __future__ import annotations

import re
import typing

from teraflashpy import Command
from teraflashpy.commands import (
    AcquisitionAverageInput,
    AcquisitionBeginInput,
    AcquisitionRangeInput,
    CommandInput,
    LaserSetInput,
    NoInput,
    SystemMonitorInput,
)

REGEX_EXPR = r"""
((SYSTEM) : ((STOP)|(TELL STATUS)|((MONITOR) (\d+))|(TIA FULL)|(TIA ATN1)|(TIA ATN2)))
|
((LASER) : ((OFF)|(ON)|((SET) ([+-]?([0-9]*[.])?[0-9]+))))
|
((ACQUISITION) : (((BEGIN) ([+-]?([0-9]*[.])?[0-9]+))|((RANGE) (\d+))|(STOP)|(START)|((AVERAGE) (\d+))|(RESET AVG)))
|
((TRANSMISSION) : ((SLIDING)|(BLOCK)))
""".replace("\n", "")


def parse_string(string: str) -> tuple[Command, CommandInput]:  # noqa: PLR0911
    matches = re.findall(REGEX_EXPR, string)

    for match in matches:
        system = match[:11]
        laser = match[11:20]
        acquisition = match[20:36]
        transmission = match[36:]
        if system[0]:
            match system:
                case (_, "SYSTEM", "STOP", "STOP", "", "", "", "", "", "", ""):
                    return Command.SystemStop, NoInput()
                case (_, "SYSTEM", "TELL STATUS", "", "TELL STATUS", "", "", "", "", "", ""):
                    return Command.SystemTellStatus, NoInput()
                case (_, "SYSTEM", _, "", "", _, "MONITOR", code, "", "", ""):
                    return Command.SystemMonitor, SystemMonitorInput(code=code)
                case (_, "SYSTEM", "TIA FULL", "", "", "", "", "", "TIA FULL", "", ""):
                    return Command.SystemTiaFull, NoInput()
                case (_, "SYSTEM", "TIA ATN1", "", "", "", "", "", "", "TIA ATN1", ""):
                    return Command.SystemTiaAtn1, NoInput()
                case (_, "SYSTEM", "TIA ATN2", "", "", "", "", "", "", "", "TIA ATN2"):
                    return Command.SystemTiaAtn2, NoInput()
                case _:
                    typing.assert_never(system)
        elif laser[0]:
            match laser:
                case (_, "LASER", "OFF", "OFF", "", "", "", "", ""):
                    return Command.LaserOff, NoInput()
                case (_, "LASER", "ON", "", "ON", "", "", "", ""):
                    return Command.LaserOn, NoInput()
                case (_, "LASER", _, "", "", _, "SET", pump_current, _):
                    return Command.LaserSet, LaserSetInput(pump_current=pump_current)
                case _:
                    typing.assert_never(laser)
        elif acquisition[0]:
            match acquisition:
                case (_, "ACQUISITION", _, _, "BEGIN", start_position, _, "", "", "", "", "", "", "", "", ""):
                    return Command.AcquisitionBegin, AcquisitionBeginInput(start_position=start_position)
                case (_, "ACQUISITION", _, "", "", "", "", _, "RANGE", measuring_range, "", "", "", "", "", ""):
                    return Command.AcquisitionRange, AcquisitionRangeInput(measuring_range=measuring_range)
                case (_, "ACQUISITION", "STOP", "", "", "", "", "", "", "", "STOP", "", "", "", "", ""):
                    return Command.AcquisitionStop, NoInput()
                case (_, "ACQUISITION", "START", "", "", "", "", "", "", "", "", "START", "", "", "", ""):
                    return Command.AcquisitionStart, NoInput()
                case (_, "ACQUISITION", _, "", "", "", "", "", "", "", "", "", _, "AVERAGE", num_averages, ""):
                    return Command.AcquisitionAverage, AcquisitionAverageInput(num_averages=num_averages)
                case (_, "ACQUISITION", "RESET AVG", "", "", "", "", "", "", "", "", "", "", "", "", "RESET AVG"):
                    return Command.AcquisitionResetAvg, NoInput()
                case _:
                    typing.assert_never(laser)
        elif transmission[0]:
            match transmission:
                case (_, "TRANSMISSION", "SLIDING", "SLIDING", ""):
                    return Command.TransmissionSliding, NoInput()
                case (_, "TRANSMISSION", "BLOCK", "", "BLOCK"):
                    return Command.TransmissionBlock, NoInput()
        else:
            msg = "Input string cannot be parsed to a command."
            raise ValueError(msg)
    msg = "Input string cannot be parsed to a command."
    raise ValueError(msg)


if __name__ == "__main__":
    cmd, cmd_input = parse_string("as LASER : SET .4123 asdfasfasdsa")
    print(cmd)
