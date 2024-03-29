from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from teraflashpy.client import TeraflashProClient

if TYPE_CHECKING:
    from teraflashpy.output import PulseData


def main(
    num_pulses: int,
    experiment_duration: timedelta,
    time_between_measurements: timedelta,
    data_folder: Path,
    extension: Literal[".pkl", ".parquet", ".csv", ".json"] = ".pkl",
) -> None:
    """Collects pulses from a Toptica TeraFlash Pro and saves them to a folder."""
    start_time = datetime.now(tz=timezone.utc)
    end_time = start_time + experiment_duration

    foldername = start_time.strftime("%Y%m%d")
    data_folder = data_folder / foldername
    data_folder.mkdir(exist_ok=True, parents=True)

    with TeraflashProClient() as client:
        while datetime.now(tz=timezone.utc) < end_time:
            pulses = client.read(num_pulses)

            scan_filename = datetime.now(tz=timezone.utc).strftime("%H-%M-%S-%f")
            save_path = (data_folder / scan_filename).with_suffix(extension)

            _write_to_file(pulses, save_path)
            time.sleep(time_between_measurements.total_seconds())


def _write_to_file(pulses: list[PulseData], save_path: Path) -> None:
    extension = save_path.suffix
    if extension == ".pkl":
        import pickle

        with save_path.open("wb") as handle:
            pickle.dump([pulse.model_dump() for pulse in pulses], handle)
    elif extension == ".parquet":
        try:
            import pyarrow as pa
            import pyarrow.parquet as pq
        except ImportError as e:
            msg = "Could not import module `pyarrow`. To save data to parquet, install it with `pip install pyarrow`."
            raise ImportError(
                msg,
                name=e.name,
                path=e.path,
            ) from e

        table = pa.Table.from_pylist([pulse.model_dump() for pulse in pulses])
        pq.write_table(table, save_path)
    elif extension == ".csv":
        import csv

        with save_path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(pulses[0].model_fields.keys()))
            writer.writeheader()
            writer.writerows([pulse.model_dump() for pulse in pulses])
    elif extension == ".json":
        import json

        with save_path.open("w") as handle:
            json.dump([pulse.model_dump(mode="json") for pulse in pulses], handle)


if __name__ == "__main__":
    main(
        num_pulses=1000,
        experiment_duration=timedelta(hours=1),
        time_between_measurements=timedelta(minutes=5),
        data_folder=Path.home() / "Desktop",
    )
