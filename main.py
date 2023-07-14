import time

from pymata4 import pymata4


TRIGGER_PIN = 2
ECHO_PIN = 4
LED_PIN = 5

board = pymata4.Pymata4()


def sonar_callback(data):
    print(f'Distance: {data[2]}cm')
    # tim


board.set_pin_mode_sonar(TRIGGER_PIN, ECHO_PIN, sonar_callback)

board.set_pin_mode_digital_output(LED_PIN)

while True:
    # print(f'Main loop start')

    board.digital_write(LED_PIN, 1)
    time.sleep(3)
    board.sonar_read(TRIGGER_PIN)

    board.digital_write(LED_PIN, 0)

    time.sleep(5)