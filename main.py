import time

from pymata4 import pymata4
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from volume_controller import IAudioEndpointVolume
from constants import TRIGGER_PIN, ECHO_PIN, LED_PIN, SONAR_TIMEOUT, MAX_DISTANCE, MIN_DISTANCE
import comtypes


def normalize_absolute_distance(distance: int):
    # Linearly converts absolute distance value to 0-1 range
    value = (MAX_DISTANCE - MIN_DISTANCE) / (MAX_DISTANCE - MIN_DISTANCE) * (distance - MAX_DISTANCE) + MAX_DISTANCE
    return round(value, 2)

def convert_normalized_distance_to_decibels(normalized_distance: float):
    # Distance is a linear value, while volume is measured in decibels and they are non-linear
    # so just doing ` normalized_distance * max_decibels ` will work as shit and special formula should be used

    # print(f'Normalized: {normalized_distance}; Calc value real: {value}')
    # return -(value.real + value.imag)

    # 0.6 = root(2 ^ x, 10)

    from sympy.solvers import solve
    from sympy.abc import x, y
    from sympy import Symbol, Eq, root

    equality = Eq(normalized_distance, root(2**x, 10))  # performs math more or less ok, but too slow
    return solve(equality, x)[0]

def set_volume_according_to_height(height):
    normalized = normalize_absolute_distance(height)

    comtypes.CoInitialize()
    ev = IAudioEndpointVolume.get_default()
    ev.SetMasterVolumeLevelScalar(normalized)

    comtypes.CoUninitialize()
    print(f'Volume set to: {normalized} dB')#; Decibels calculated: {decibels}')

def sonar_callback(data):
    board.digital_write(LED_PIN, 1)
    print(f'Distance: {data[2]}cm;')# Volume: {volume.process_volume()}')
    board.digital_write(LED_PIN, 0)
    set_volume_according_to_height((data[2] * 4) / 100)

def setup_arduino():
    arduino = pymata4.Pymata4()

    arduino.set_pin_mode_sonar(TRIGGER_PIN, ECHO_PIN, sonar_callback, timeout=SONAR_TIMEOUT)
    arduino.set_pin_mode_digital_output(LED_PIN)


    return arduino


import comtypes




# volume = AudioController('chrome.exe')




board = setup_arduino()
while True:
    pass  #

    time.sleep(5)

