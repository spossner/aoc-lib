from itertools import chain

from aoc import Point, Rect


def test_rect():
    r1 = Rect(5, 5, 30, 30)
    r2 = Rect(15, 15, 30, 30)
    r3 = Rect(15, 15, 30, 30)
    assert r1 != r2
    assert r2 == r3
    assert r2 not in r1
    assert r3 in r2
    assert (5, 5) in r1
    assert (34, 34) in r1
    assert (35, 35) not in r1
    assert Point(5, 5) in r1
    assert Point(34, 34) in r1
    assert Point(35, 35) not in r1


def test_contains():
    r = Rect(490, 0, 74, 162)
    p = Point(556, 124)
    assert p in r
    p2 = Point(544, 162)
    assert p2 not in r
    r.extend(p2)
    assert p2 in r


def test_extend():
    r1 = Rect(5, 5, 10, 10)
    p_out = (
        Point(3, 3), Point(15, 5), Point(5, 15), Point(15, 15),
        Point(0, 0), Point(23, 34), Point(23, 2), Point(20, 34)
    )
    p_still_out = (Point(-1, 3), Point(15, -1), Point(24, 15), Point(20, 35))
    p_in = (Point(5, 5), Point(6, 5), Point(14, 5), Point(5, 14), Point(14, 14))
    for p in p_in:
        assert p in r1, "{p} should be inside {r1}"
    for p in chain(p_out, p_still_out):
        assert p not in r1, "{p} should not be inside {r1}"
    for p in p_out:
        r1.extend(p)
    for p in p_in:
        assert p in r1, "{p} should be inside {r1}"
    for p in p_out:
        assert p in r1, "{p} should now be inside {r1}"
    for p in p_still_out:
        assert p not in r1, "{p} should still not be inside {r1}"


def test_empty_rect():
    empty = Rect()
    assert bool(empty) is False
    p = Point(556, 124)
    empty.extend(p)
    assert p in empty
    p2 = Point(500, 100)
    empty.extend(p2)
    assert p in empty
    assert p2 in empty
    assert Point(520, 110) in empty


def test_rect_intersection():
    r1 = Rect(5, 5, 30, 30)
    r2 = Rect(15, 15, 30, 30)
    r_i = r1.intersection(r2)
    r_j = r2.intersection(r1)
    assert r_i in r1
    assert r_j in r1
    assert r_i in r2
    assert r_j in r2
    assert r_i in r_i
    assert r_j in r_j
    assert r_i in r_j
    assert r_j in r_i
    assert r_i == r_j


def test_rect_extend():
    r1 = Rect(5, 5, 30, 30)
    r1.extend(Point(1, 1))
    assert Point(34, 34) in r1
    assert Point(35, 35) not in r1
    assert r1.x == 1
    assert r1.y == 1
    assert Point(34, 34) in r1
    assert Point(35, 35) not in r1

    r2 = Rect(5, 5, 30, 30)
    r2.extend([23, 20])
    r2.extend((2, 2))
    assert Point(34, 34) in r2
    assert Point(35, 35) not in r2


def test_rect_multi_extend():
    r1 = Rect(5, 5, 30, 30)
    r1.extend(Point(1, 1), Point(40, 40), Point(50, 50), (60, 60), [70, 70, 70])
    assert Point(34, 34) in r1
    assert Point(70, 70) in r1
    assert Point(0, 0) not in r1


def test_rect_extend_list_mixed():
    r1 = Rect(5, 5, 30, 30)
    r1.extend(
        (Point(1, 1), Point(40, 40), Point(50, 50), (60, 60), [70, 70, 70]),
        Point(80, 80),
        [Point(90, 90)],
    )
    assert Point(34, 34) in r1
    assert Point(70, 70) in r1
    assert Point(0, 0) not in r1
