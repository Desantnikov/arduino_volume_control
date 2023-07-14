import time
from threading import Thread

from pymata4 import pymata4


trigger_pin = 2
echo_pin = 4
led_pin = 5

board = pymata4.Pymata4()


def the_callback(data):

    print(f'Distance: {data[2]}cm')
    # tim


# board.digital_write(led_pin, 1)
board.set_pin_mode_sonar(trigger_pin, echo_pin, the_callback)
board.set_pin_mode_digital_output(led_pin)

while True:
    print('lOOP MAIN START')
    try:
        board.digital_write(led_pin, 1)
        time.sleep(3)
        board.sonar_read(trigger_pin)

        board.digital_write(led_pin, 0)
    except:
        print(f'All broken')
        board.shutdown()

    time.sleep(5)