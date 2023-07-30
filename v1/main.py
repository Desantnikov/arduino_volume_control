import time
from pymata4 import pymata4

from utils import normalize_distance
from shared.volume_controller import VolumeController
from constants import TRIGGER_PIN, ECHO_PIN, SONAR_TIMEOUT, LED_PIN, MIN_DISTANCE_CM, MAX_DISTANCE_CM


def sonar_callback(data):
    board.digital_write(LED_PIN, 1)
    board.digital_write(LED_PIN, 0)

    current_distance = data[2]

    # normalized distance is a float in range 0-1
    normalized_distance = normalize_distance(current_distance, MIN_DISTANCE_CM, MAX_DISTANCE_CM)

    # 100% means hand has been removed
    if normalized_distance == 1:  # TODO: rework this hand removal detection way to make it possible to set 100% volume
        print(f'Hand returned, ignore')
        return

    VolumeController().set_system_volume(normalized_distance)

    print(f'Distance: {data[2]}cm; Set {normalized_distance}% of volume;\r\n')


if __name__ == "__main__":
    try:
        board = pymata4.Pymata4()
        board.set_pin_mode_sonar(TRIGGER_PIN, ECHO_PIN, sonar_callback, timeout=SONAR_TIMEOUT)
        board.set_pin_mode_digital_output(LED_PIN)

        while True:
            pass

            time.sleep(5)

    except Exception as e:
        print(f'\r\nProgram failed with exception: {e}\r\nPress any key to finish\r\n')
        input()
