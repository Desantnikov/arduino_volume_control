# Arduino board
# ------------
TRIGGER_PIN = 2
ECHO_PIN = 4
LED_PIN = 5

# Sonar
# ------------
MAX_DISTANCE = 26  # distance measured by sonar when no hand is inside the box
MIN_DISTANCE = 6  # distance measured by sonar when hand is in the lowest position

AVERAGE_HAND_HEIGHT = 3  # to use as a thresholds

# Default 80 000 timeout equals max distance about 260 cm, while box is not so big.
# Timeout 2200 equals max distance 39 cm. For some reasons timeouts < 2200 make sonar stop collecting any data
SONAR_TIMEOUT = 2200


# Sound
# ------------

