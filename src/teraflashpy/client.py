from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from multiprocessing import Process, Queue
from typing import TYPE_CHECKING

import numpy as np

from teraflashpy import ACQUISITION_PORT_MAP, LOCALHOST, AcquisitionMode
from teraflashpy.output import PulseData

if TYPE_CHECKING:
    from types import TracebackType

logger = logging.getLogger(__name__)


async def _collect_data(queue: Queue) -> None:
    reader, writer = await asyncio.open_connection(LOCALHOST, ACQUISITION_PORT_MAP[AcquisitionMode.Asynchronous])
    try:
        while True:
            length_data_bytes = await reader.readexactly(6)
            length_data = int(length_data_bytes.decode("utf-8"))
            pulse_data_bytes = await reader.readexactly(length_data)
            timestamp = datetime.now(tz=timezone.utc)
            queue.put((pulse_data_bytes, timestamp))
    except Exception:
        logger.exception(
            {
                "length_data_bytes": length_data_bytes if "length_data_bytes" in locals() else None,
                "length_data": length_data if "length_data" in locals() else None,
                "pulse_data_bytes": pulse_data_bytes if "pulse_data_bytes" in locals() else None,
            },
        )
    finally:
        writer.close()
        await writer.wait_closed()


class TeraflashProClient:
    def __enter__(self):
        self.queue: Queue[tuple[bytes, datetime]] = Queue()
        self.process = Process(target=self.run_backend, args=(self.queue,))
        self.process.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        self.process.terminate()

    @staticmethod
    def run_backend(queue: Queue[tuple[bytes, datetime]]) -> None:
        asyncio.run(_collect_data(queue))

    @staticmethod
    def _decode_pulse(pulse: bytes) -> tuple[list[str], np.ndarray, np.ndarray]:
        pulsedata = pulse.decode("utf-8").split("\r\n")
        header = pulsedata.pop(0).split(",")
        time = np.zeros(len(pulsedata) - 1, dtype=float)
        magnitude = np.zeros(len(pulsedata) - 1, dtype=float)
        for x in range(len(pulsedata) - 1):
            _time, _magnitude = pulsedata[x].split(",")
            time[x] = float(_time)
            magnitude[x] = float(_magnitude)

        return header, time, magnitude

    def _clear_queue(self) -> None:
        while True:
            if self.queue.empty():
                break
            self.queue.get_nowait()

    def read(self, num_pulses: int, timeout: int = 20) -> list[PulseData]:
        self._clear_queue()

        pulses = []
        for _ in range(num_pulses):
            pulse_bytes, timestamp = self.queue.get(timeout=timeout)
            header, time, magnitude = self._decode_pulse(pulse_bytes)
            pulse = PulseData(timestamp=timestamp, header=header, time=time, magnitude=magnitude)
            pulses.append(pulse)

        return pulses
