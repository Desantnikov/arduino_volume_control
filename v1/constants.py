# Arduino board
# ------------
TRIGGER_PIN = 2
ECHO_PIN = 4
LED_PIN = 5

# Sonar
# ------------
MAX_DISTANCE_CM = 25  # distance measured by sonar when no hand is inside the box
MIN_DISTANCE_CM = 7  # distance measured by sonar when hand is in the lowest position


# Default 80 000 timeout equals max distance about 260 cm, while box is not so big.
# Timeout 2200 equals max distance 39 cm. For some reasons timeouts < 2200 make sonar stop collecting any data
SONAR_TIMEOUT = 2200
