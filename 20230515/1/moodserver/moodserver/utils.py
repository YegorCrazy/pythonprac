"""Utils module."""


def InvertCoordinates(const_coord):
    """Invert coordinates arrayand return a copy."""
    coord = const_coord.copy()
    coord[0], coord[1] = coord[1], coord[0]
    return coord
