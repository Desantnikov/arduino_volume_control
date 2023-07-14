import threading
import time
from threading import Thread

from pymata4 import pymata4


trigger_pin = 2
echo_pin = 4
led_pin = 5

board = pymata4.Pymata4()

board.set_pin_mode_digital_output(led_pin)

def the_callback(data):
    # board.digital_write(led_pin, 0)
    print(f'Distance: {data[2]}cm')
    # tim


def main_thread():
    while True:
        print('lOOP MAIN START')
        try:
            board.sonar_read(trigger_pin)
        except:
            print(f'All broken')
            board.shutdown()

        time.sleep(5)


def second_thread():
    print('Second thread')
    board.digital_write(led_pin, 1)
    time.sleep(5)
    board.digital_write(led_pin, 0)


# board.digital_write(led_pin, 1)
board.set_pin_mode_sonar(trigger_pin, echo_pin, the_callback)


main_thread = threading.Thread(target=main_thread)
secondary_thread = threading.Thread(target=second_thread)
secondary_thread.start()

main_thread.start()