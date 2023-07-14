import time
from pymata4 import pymata4

from utils import normalize_absolute_distance, set_system_volume
from constants import TRIGGER_PIN, ECHO_PIN, SONAR_TIMEOUT, LED_PIN


def sonar_callback(data):
    board.digital_write(LED_PIN, 1)
    board.digital_write(LED_PIN, 0)

    current_distance = data[2]

    normalized_distance = normalize_absolute_distance(current_distance)  # float in range 0-1
    set_system_volume(normalized_distance)
    print(f'Distance: {data[2]}cm; Set {normalized_distance}% of volume;\r\n')


if __name__ == "__main__":
    board = pymata4.Pymata4()
    board.set_pin_mode_sonar(TRIGGER_PIN, ECHO_PIN, sonar_callback, timeout=SONAR_TIMEOUT)
    board.set_pin_mode_digital_output(LED_PIN)

    while True:
        pass

        time.sleep(5)

