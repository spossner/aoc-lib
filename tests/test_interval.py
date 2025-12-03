from aoc import Interval


def test_creation():
    i = Interval(5, 10)
    assert i.start == 5
    assert i.end == 10


def test_creation_swapped():
    i = Interval(10, 5)
    assert i.start == 5
    assert i.end == 10


def test_from_length():
    i = Interval.from_length(5, 10)
    assert i.start == 5
    assert i.end == 14
    assert i.length == 10


def test_length():
    assert Interval(5, 10).length == 6
    assert len(Interval(5, 10)) == 6
    assert Interval(5, 5).length == 1


def test_contains_value():
    i = Interval(5, 10)
    assert 5 in i
    assert 7 in i
    assert 10 in i
    assert 4 not in i
    assert 11 not in i


def test_contains_interval():
    outer = Interval(0, 100)
    inner = Interval(25, 75)
    assert inner in outer
    assert outer not in inner

    same = Interval(0, 100)
    assert same in outer


def test_iteration():
    i = Interval(3, 7)
    assert list(i) == [3, 4, 5, 6, 7]


def test_overlaps():
    a = Interval(0, 10)
    b = Interval(5, 15)
    c = Interval(11, 20)
    d = Interval(10, 12)

    assert a.overlaps(b)
    assert b.overlaps(a)
    assert not a.overlaps(c)
    assert a.overlaps(d)  # shares endpoint 10


def test_adjacent():
    a = Interval(0, 10)
    b = Interval(11, 20)
    c = Interval(12, 20)

    assert a.adjacent(b)
    assert b.adjacent(a)
    assert not a.adjacent(c)


def test_intersection():
    a = Interval(0, 10)
    b = Interval(5, 15)
    c = Interval(20, 30)

    result = a.intersection(b)
    assert result == Interval(5, 10)
    assert a & b == Interval(5, 10)

    assert a.intersection(c) is None
    assert a & c is None


def test_union():
    a = Interval(0, 10)
    b = Interval(5, 15)
    c = Interval(11, 20)
    d = Interval(30, 40)

    assert a.union(b) == Interval(0, 15)
    assert a | b == Interval(0, 15)

    # Adjacent intervals can be merged
    assert a.union(c) == Interval(0, 20)

    # Non-overlapping, non-adjacent returns None
    assert a.union(d) is None


def test_difference():
    a = Interval(0, 100)
    b = Interval(25, 75)

    result = a.difference(b)
    assert len(result) == 2
    assert result[0] == Interval(0, 24)
    assert result[1] == Interval(76, 100)
    assert a - b == result

    # No overlap
    c = Interval(200, 300)
    assert a.difference(c) == [a]

    # Complete overlap
    d = Interval(0, 100)
    assert a.difference(d) == []


def test_split_at():
    i = Interval(0, 100)

    left, right = i.split_at(50)
    assert left == Interval(0, 49)
    assert right == Interval(50, 100)

    # Split at start
    left, right = i.split_at(0)
    assert left is None
    assert right == i

    # Split past end
    left, right = i.split_at(200)
    assert left == i
    assert right is None


def test_clamp():
    i = Interval(10, 20)
    assert i.clamp(5) == 10
    assert i.clamp(15) == 15
    assert i.clamp(25) == 20


def test_expand():
    i = Interval(10, 20)
    expanded = i.expand(5)
    assert expanded == Interval(5, 25)


def test_shift():
    i = Interval(10, 20)
    assert i.shift(5) == Interval(15, 25)
    assert i + 5 == Interval(15, 25)
    assert i + (-5) == Interval(5, 15)


def test_immutable():
    i = Interval(5, 10)
    # Should be hashable (frozen dataclass)
    s = {i}
    assert i in s
