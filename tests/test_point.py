from aoc import (
    Point,
    Point3d,
    all_adjacent_iter,
    direct_adjacent_iter,
    iter_from_to,
    length,
    manhattan_distance,
    rot_ccw,
    rot_cw,
)


def test_rotation_cw():
    assert rot_cw(Point(0, 1)) == (-1, 0)


def test_rotation_ccw():
    assert rot_ccw(Point(0, 1)) == (1, 0)
    assert rot_ccw(Point(1, 0)) == (0, -1)


def test_length():
    assert length((1, 2, -3)) == 6
    assert length(Point3d(1, 2, -3)) == 6
    assert length(Point(-2, -4)) == 6


def test_manhattan_distance():
    assert manhattan_distance((1, 2, -3), (2, 0, -3)) == 3
    assert manhattan_distance(Point3d(1, 2, -3), Point3d(-1, -1, -1)) == 7
    assert manhattan_distance(Point(-2, -4), Point(0, -1)) == 5


def test_adjacents():
    expected_all = {(11, 4), (12, 4), (13, 4), (11, 5), (13, 5), (11, 6), (12, 6), (13, 6)}
    assert len(set(all_adjacent_iter(Point(12, 5))).difference(expected_all)) == 0

    expected_direct = [(12, 4), (11, 5), (13, 5), (12, 6)]
    assert len(set(direct_adjacent_iter(Point(12, 5))).difference(expected_direct)) == 0


def test_iter_from_to():
    assert list(iter_from_to(Point(300, 5), Point(304, 5))) == [
        (300, 5), (301, 5), (302, 5), (303, 5), (304, 5)
    ]
    assert list(iter_from_to(Point(300, 8), Point(300, 5))) == [
        (300, 8), (300, 7), (300, 6), (300, 5)
    ]
    assert list(iter_from_to(Point(305, 5), Point(300, 0))) == [
        (305, 5), (304, 4), (303, 3), (302, 2), (301, 1), (300, 0)
    ]
