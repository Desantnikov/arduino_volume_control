import time

from pymata4 import pymata4


trigger_pin = 2
echo_pin = 4
led_pin = 5

board = pymata4.Pymata4()


def the_callback(data):
    # board.digital_write(led_pin, 0)
    print(f'Distance: {data[2]}cm')
    # tim


# board.digital_write(led_pin, 1)
board.set_pin_mode_sonar(trigger_pin, echo_pin, the_callback)

while True:
    print('lOOP START')
    try:

        # time.sleep(4)



        board.sonar_read(trigger_pin)


    except:
        print(f'All broken')
        board.shutdown()

    time.sleep(5)