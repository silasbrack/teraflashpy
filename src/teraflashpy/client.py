import asyncio
import socket
import typing

import numpy as np

from teraflashpy import ACQUISITION_PORT_MAP, LOCALHOST, AcquisitionMode, PulseData
from teraflashpy.core import Config


def _collect_pulse_data(acquisition_mode: AcquisitionMode) -> PulseData:
    teraflash_server_port = ACQUISITION_PORT_MAP[acquisition_mode]
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((LOCALHOST, teraflash_server_port))

    length_data = client.recv(6)
    pulsedata = client.recv(int(length_data.decode("utf-8")))
    client.close()

    pulsedata = pulsedata.decode("utf-8").split("\r\n")
    header = pulsedata.pop(0)
    time = np.zeros(len(pulsedata) - 1, dtype=float)
    magnitude = np.zeros(len(pulsedata) - 1, dtype=float)
    for x in range(len(pulsedata) - 1):
        time[x] = float(pulsedata[x].split(",")[0])
        magnitude[x] = float(pulsedata[x].split(",")[1])

    return PulseData(header=header, time=time, magnitude=magnitude)


def collect_pulse_data() -> PulseData:
    return _collect_pulse_data(acquisition_mode=AcquisitionMode.Synchronous)


async def collect_pulse_data_async() -> PulseData:
    return _collect_pulse_data(acquisition_mode=AcquisitionMode.Asynchronous)


async def run(config: Config) -> PulseData:
    match config.acquisition_mode:
        case AcquisitionMode.Synchronous:
            return collect_pulse_data()
        case AcquisitionMode.Asynchronous:
            return await collect_pulse_data_async()
        case _:
            typing.assert_never(config.acquisition_mode)


if __name__ == "__main__":
    config = Config()
    asyncio.run(run(config))
