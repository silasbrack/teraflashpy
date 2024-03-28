import os
import pickle
import time
from datetime import datetime

from teraflashpy.client import TeraflashProClient


def main():
    def save_data(data, foldername, filename):
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        with open(f"{foldername}/{filename}.pkl", "wb") as handle:
            pickle.dump(data, handle)
        return print("data saved", filename)

    foldername = datetime.now().strftime("%Y%m%d")

    total_minutes = 60  # how many minutes for the measurement
    minutes_between_measurements = 5

    t_end = time.time() + 60 * total_minutes

    with TeraflashProClient() as client:
        while time.time() < t_end:
            pulses = client.read(num_pulses=1000)

            folder_path = f"c:/Users/s161896/Desktop/{foldername}"
            scan_filename = datetime.now().strftime("%H-%M-%S-%f")
            save_data([pulse.model_dump() for pulse in pulses], folder_path, scan_filename)
            time.sleep(60 * minutes_between_measurements)


if __name__ == "__main__":
    main()
