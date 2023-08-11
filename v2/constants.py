# unlike v1,
# !! v2 uses millimeters !!
# ------------

MAX_DISTANCE_MM = 275  # too big max distance leads to issues when setting volume to low
MIN_DISTANCE_MM = 35  # distance measured by sonar when hand is in the lowest position
DEFAULT_SERIAL_PORT_NAME = "COM3"

VIBRO_DOUBLECLICK_MAX_TIME = 1  # two clicks in less than 1 second will be considered a doubleclick
# sometimes, if placed not on hard surface, sensor keeps moving after first click and it's counted as a second click
VIBRO_DOUBLECLICK_MIN_TIME = 0.20  # two clicks on less than 0.2 seconds will be considered a fake measurement
INTERVAL_BETWEEN_DOUBLECLICKS = 1.75  # ignore all (mainly fake) doubleclicks for 1.75 sec's after last doubleclick

ROUND_VOLUME_VALUE_TO_N_DIGITS = 1
IGNORABLE_VOLUME_DIFFERENCE = 0.05  # when current volume differs from new volume in less than 0.05 - ignore it
