import time

import serial

from v1.utils import normalize_distance
from shared.volume_controller import VolumeController
from v2.constants import MIN_DISTANCE_MM, MAX_DISTANCE_MM, DEFAULT_SERIAL_PORT_NAME


def start_event_loop():
    while True:
        device_response = device.readline()
        print(f'Raw device response: {device_response}')

        if "Vibro" not in device_response.decode() and "Distance" not in device_response.decode():
            print(f'Invalid data, skip line')
            continue

        # take first word to understand which data is sent in this line
        first_word = device_response.decode().split()[0].strip(':').lower()

        if first_word == "distance":  # if got "Distance: 34\r\n" from arduino
            current_distance_mm = int(device_response.decode().split()[-1])  # extract distance value

            # convert absolute distance value to float in [0:1] range, which is required by the volume controller class
            new_volume_level = normalize_distance(current_distance_mm, MIN_DISTANCE_MM, MAX_DISTANCE_MM)

            # 1 means maximum distance which means hand has been removed
            if new_volume_level == 1:
                print(f'Hand returned, ignore')
                continue

            VolumeController().set_system_volume(new_volume_level)

        elif first_word == "vibro":  # if got `Vibro: true/false \r\n` from arduino
            is_vibro_happened = bool(device_response.decode().split()[-1])  # extract distance value

            print(f'\r\n\r\nVIBRO HAPPENED\r\n\r\n')


if __name__ == "__main__":
    serial_port_name = input(f"Enter serial port to use. Use default ({DEFAULT_SERIAL_PORT_NAME}) if blank:\r\n")
    serial_port_name = serial_port_name or DEFAULT_SERIAL_PORT_NAME

    device = serial.Serial(serial_port_name)
    print(f'Device connected: {device}')

    try:
        start_event_loop()

    finally:
        device.close()
