import comtypes
from volume_controller import IAudioEndpointVolume

from constants import MIN_DISTANCE, MAX_DISTANCE


def normalize_absolute_distance(distance: int):
    # Linearly converts absolute distance value to 0-1 range
    value = ((distance - MIN_DISTANCE) / (MAX_DISTANCE - MIN_DISTANCE)) * (1 - 0) + 0

    if value < 0:
        value = 0
    if value > 1:
        value = 1

    return value


def set_system_volume(volume: float):
    comtypes.CoInitialize()
    ev = IAudioEndpointVolume.get_default()
    ev.SetMasterVolumeLevelScalar(volume)
    comtypes.CoUninitialize()
