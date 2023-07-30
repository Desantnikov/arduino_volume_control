def normalize_distance(distance: int, min_distance: int, max_distance: int):
    # Linearly converts absolute distance value to [0:1] range according to max and min distance
    value = ((distance - min_distance) / (max_distance - min_distance)) * (1 - 0) + 0

    if value < 0:
        value = 0
    if value > 1:
        value = 1

    return value

