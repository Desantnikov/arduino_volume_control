import time

from shared.volume_controller import VolumeController
from shared.keyboard_controller import SendInput, Keyboard, VK_MEDIA_PLAY_PAUSE
from v1.utils import normalize_distance
from v2.constants import MIN_DISTANCE_MM, MAX_DISTANCE_MM, VIBRO_DOUBLECLICK_MAX_TIME, VIBRO_DOUBLECLICK_MIN_TIME, INTERVAL_BETWEEN_DOUBLECLICKS


class DeviceResponsesHandler:

    def __init__(self):
        self.first_word_to_handler_function = {
            "distance": self.handle_distance,
            "vibro": self.handle_vibro,
            "invalid": self.handle_invalid
        }

        self.volume_controller = VolumeController()

        self.last_vibro_timestamp = 0
        self.last_doubleclick_timestamp = 0

    def get_handler_function(self, device_response: str):
        splitted_response = device_response.split()

        first_word = "invalid"
        if splitted_response:
            # take first word to understand which data is sent in this line
            first_word = splitted_response[0].strip(':').lower()

        return self.first_word_to_handler_function.get(first_word)

    def handle_distance(self, device_response: str):
        current_distance_mm = int(device_response.split()[-1])  # extract distance value

        # convert absolute distance value to float in [0:1] range, which is required by the volume controller class
        new_volume_level = normalize_distance(current_distance_mm, MIN_DISTANCE_MM, MAX_DISTANCE_MM)

        # 1 means maximum distance which means hand has been removed
        if new_volume_level == 1:
            # print(f'Hand returned, ignore')
            return

        self.volume_controller.set_system_volume(new_volume_level)

    def handle_vibro(self, device_response: str):
        time_between_last_vibros = time.time() - self.last_vibro_timestamp
        print(f'Time between: {time_between_last_vibros};')

        time_between_last_doubleclick = time.time() - self.last_doubleclick_timestamp

        time_between_last_vibros_ok = VIBRO_DOUBLECLICK_MIN_TIME < time_between_last_vibros < VIBRO_DOUBLECLICK_MAX_TIME
        time_between_last_doubleclick_ok = time_between_last_doubleclick < INTERVAL_BETWEEN_DOUBLECLICKS

        if time_between_last_vibros_ok:
            if time_between_last_doubleclick_ok:
                print(f'DOUBLECLICK TOO EARLY, IGNORE')

                return

            SendInput(Keyboard(VK_MEDIA_PLAY_PAUSE))  # play/pause active media (video, music, etc)
            self.last_doubleclick_timestamp = time.time()
            print(f'DOUBLECLICK: SENT A PLAY/PAUSE\r\n\r\n')

        self.last_vibro_timestamp = time.time()

    @staticmethod
    def handle_invalid(device_response: str):
        print(f"Warning:\r\nGot invalid data from arduino: {device_response}\r\n\r\n")

