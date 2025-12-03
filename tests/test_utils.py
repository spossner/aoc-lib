from aoc import batched, fetch, get_ints, range_intersect


def test_fetch():
    assert list(fetch([3], 2)) == [3, None]
    assert list(fetch([3], 2, 0)) == [3, 0]
    assert list(fetch([3, 4], 2)) == [3, 4]
    assert list(fetch([3, 4, 5], 2)) == [3, 4]
    assert list(fetch([3, 4, 5], 10, 0)) == [3, 4, 5, 0, 0, 0, 0, 0, 0, 0]


def test_get_ints():
    assert get_ints("Set value to 2 and jump -34.") == [2, -34]


def test_batched():
    assert list(batched("ABCDEFG", 3)) == [["A", "B", "C"], ["D", "E", "F"], ["G"]]


def test_range_intersection():
    r1 = range(1, 100)
    r2 = range(50, 150)

    assert range_intersect(r1, r2) == range(50, 100)
    assert range_intersect(r1, r1) == r1
    assert range_intersect(r2, r2) == r2
    assert range_intersect(r1, range(200, 300)) is None
    assert range_intersect(r1, None) is None
    assert range_intersect(None, r2) is None
    assert range_intersect(None, None) is None
    assert range_intersect(r1, range(0, 1)) is None
    assert range_intersect(r1, range(0, 2)) == range(1, 2)
