from shared.volume_controller import VolumeController
from v1.utils import normalize_distance
from v2.constants import MIN_DISTANCE_MM, MAX_DISTANCE_MM


class DeviceResponsesHandler:
    @classmethod
    def get_handler_function(cls, device_response: str):
        first_word_to_handler_function = {
            "distance": cls.handle_distance,
            "vibro": cls.handle_vibro,
            "invalid": cls.handle_invalid
        }

        # take first word to understand which data is sent in this line
        first_word = device_response.split()[0].strip(':').lower()

        return first_word_to_handler_function.get(first_word) or first_word_to_handler_function["invalid"]

    @staticmethod
    def handle_distance(device_response: str):
        current_distance_mm = int(device_response.split()[-1])  # extract distance value

        # convert absolute distance value to float in [0:1] range, which is required by the volume controller class
        new_volume_level = normalize_distance(current_distance_mm, MIN_DISTANCE_MM, MAX_DISTANCE_MM)

        # 1 means maximum distance which means hand has been removed
        if new_volume_level == 1:
            # print(f'Hand returned, ignore')
            return

        VolumeController().set_system_volume(new_volume_level)

    @staticmethod
    def handle_vibro(device_response: str):
        is_vibro_happened = bool(device_response.split()[-1])  # extract distance value

        print(f'\r\n\r\nVIBRO HAPPENED\r\n\r\n')

    @staticmethod
    def handle_invalid(device_response: str):
        print(f"Warning:\r\nGot invalid data from arduino: {device_response}\r\n\r\n")

