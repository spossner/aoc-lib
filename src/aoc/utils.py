import re
from itertools import chain, islice


def get_ints(s: str) -> list[int]:
    """
    Get all int (including sign) values from the given string
    """
    return list(map(int, re.findall(r"((?:-|\+)?\d+)", s)))

def build_number(*arrays: list[int], base=10) -> int:
    """
    Build a number from the given arrays
    :param arrays: the arrays containing the single digits of the desired number
    :param base: the base of the number represented in the arrays (defaults to 10)
    :return: the number as int
    """
    factor = 1
    result = 0
    for arr in reversed(arrays):
        for num in reversed(arr):
            result += num * factor
            factor *= base
    return result


def fetch(iterable, n: int, fillvalue=None) -> list:
    """
    fetches n values from iterable - filled with fillvalue if needed;
    great for destructuring data with different number of arguments etc
    e.g.: a, b = fetch(args, 2) - fetches 2 elements from args and fills with None if needed

    :param iterable: the iterable to fetch from
    :param n: the number of elements to fetch; align that with your destructuring
    :param fillvalue: optional fill value if less than n elements are available (None as default)
    :return: list with the n elements; filled with fillvalue if needed
    """
    if len(iterable) >= n:
        return iterable[0:n]
    fill = [fillvalue] * (n - len(iterable))
    return list(chain(iterable, fill))


def batched(iterable, n):
    "Batch data into lists of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := list(islice(it, n)):
        yield batch


def range_intersect(r1, r2):
    """Return overlap range for two range objects of same step or None if no overlap."""
    if r1 is None or r2 is None:
        return None
    if r1.step != r2.step:
        raise ValueError("ranges must have same step")
    return range(max(r1.start, r2.start), min(r1.stop, r2.stop), r1.step) or None


def split_range(r1, r2):
    """
    Return a triple of (left, overlap, right) ranges for two given ranges r1 and r2
    or None if there is no overlap. Non-existing ranges are None.
    """
    overlap = range_intersect(r1, r2)
    if overlap is None:
        return None

    r_left = range(r1.start, overlap.start) or None
    r_right = range(overlap.stop, r1.stop) or None

    return (r_left, overlap, r_right)
