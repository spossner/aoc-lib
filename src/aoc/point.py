import math
from collections import namedtuple

Point = namedtuple("Point", "x,y", defaults=[0, 0])
Point3d = namedtuple("Point3d", "x,y,z", defaults=[0, 0, 0])

NORTH = Point(0, -1)
EAST = Point(1, 0)
SOUTH = Point(0, 1)
WEST = Point(-1, 0)
NORTH_WEST = Point(-1, -1)
NORTH_EAST = Point(1, -1)
SOUTH_WEST = Point(-1, 1)
SOUTH_EAST = Point(1, 1)

DIRECT_ADJACENTS = (NORTH, EAST, SOUTH, WEST)  # 4 adjacent nodes
ALL_ADJACENTS = (NORTH, NORTH_EAST, EAST, SOUTH_EAST, SOUTH, SOUTH_WEST, WEST, NORTH_WEST)
ADJACENTS_3D = (
    Point3d(1, 0, 0),  # RIGHT
    Point3d(-1, 0, 0),  # LEFT
    Point3d(0, -1, 0),  # ABOVE
    Point3d(0, 1, 0),  # BELOW
    Point3d(0, 0, -1),  # FRONT
    Point3d(0, 0, 1),  # BEHIND
)

OPPOSITE_DIRECTION = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

DIRECTIONS = {
    "N": NORTH, "n": NORTH, "U": NORTH, "u": NORTH, "^": NORTH,
    "S": SOUTH, "s": SOUTH, "D": SOUTH, "d": SOUTH, "v": SOUTH,
    "E": EAST, "e": EAST, "R": EAST, "r": EAST, ">": EAST,
    "W": WEST, "w": WEST, "L": WEST, "l": WEST, "<": WEST,
}


def translate(p, offset, times=1):
    if isinstance(p, Point3d):
        return Point3d(p.x + offset[0] * times, p.y + offset[1] * times, p.z + offset[2] * times)

    if isinstance(p, Point):
        return Point(p.x + offset[0] * times, p.y + offset[1] * times)

    if isinstance(p, tuple):
        assert len(p) == len(offset)
        result = []
        for i in range(len(p)):
            result.append(p[i] + offset[i] * times)
        return tuple(result)
    raise ValueError(f"can not translate {type(p)}")


def rot_cw(p: tuple) -> tuple:
    return Point(-p[1], p[0])


def rot_ccw(p: tuple) -> tuple:
    return Point(p[1], -p[0])


def length(p) -> int:
    return sum(map(abs, p))


def manhattan_distance(p1, p2) -> int:
    """
    Calculates the manhattan distance of two given tuples (may be multi dimensional).
    Note that both tuples are assumed to have same length.

    :param p1: first tuple
    :param p2: second tuple with same length than p1
    :return: the manhattan distance of both tuples
    """
    assert len(p1) == len(p2)
    ans = 0
    for i in range(len(p1)):
        ans += abs(p1[i] - p2[i])
    return ans

def distance(p1, p2) -> float:
    """
        Calculates the distance of two given tuples (may be multi dimensional).
        Note that both tuples are assumed to have same length.

        :param p1: first tuple
        :param p2: second tuple with same length than p1
        :return: the distance of both tuples
        """
    assert len(p1) == len(p2)
    ans = 0
    for i in range(len(p1)):
        ans += abs(p1[i] - p2[i]) ** 2
    return math.sqrt(ans)


def all_adjacent_iter(p: tuple, width: int = 0, height: int = 0):
    """
    Iterates all eight adjacent points of the given point (x,y)

    :param p: a tuple (or Point) with first two elements are x and y
    :param width: optional width (results will have 0 <= x < width)
    :param height: optional height (results will have 0 <= y < height)
    :return: iterator of adjacent Points
    """
    yield from _adjacent_iter(p, width, height)


def direct_adjacent_iter(p: tuple, width: int = 0, height: int = 0):
    """
    Iterates all four direct adjacent points of the given point (x,y) - no diagonals

    :param p: a tuple (or Point) with first two elements are x and y
    :param width: optional width (results will have 0 <= x < width)
    :param height: optional height (results will have 0 <= y < height)
    :return: iterator of direct adjacent Points
    """
    yield from _adjacent_iter(p, width, height, DIRECT_ADJACENTS)


def _adjacent_iter(p: tuple, width: int = 0, height: int = 0, adjacents=ALL_ADJACENTS):
    """
    Iterates the given adjacent [(dx,dy),...] points of the given point p (x,y)

    :param p: a tuple (or Point) with first two elements are x and y
    :param width: optional width (results will have 0 <= x < width)
    :param height: optional height (results will have 0 <= y < height)
    :param adjacents: the list of adjacent distances - [(dx,dy),...]
    :return: iterator of direct adjacent Points
    """
    for dx, dy in adjacents:
        np = Point(p[0] + dx, p[1] + dy)
        if width > 0 and (np.x < 0 or np.x >= width):
            continue
        if height > 0 and (np.y < 0 or np.y >= height):
            continue
        yield np


def point_by_row(self, other):
    if self[1] == other[1]:
        return self[0] - other[0]
    else:
        return self[1] - other[1]


def iter_from_to(start: Point, dest: Point):
    assert len(start) == len(dest)
    pos = start
    yield pos
    dx = dest.x - start.x
    dy = dest.y - start.y
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return
    offset = (dx / steps, dy / steps)
    for _ in range(steps):
        pos = translate(pos, offset)
        yield Point(int(pos.x), int(pos.y))
