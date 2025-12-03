from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Interval:
    """
    Inclusive interval [start, end] with integer bounds.
    """

    start: int
    end: int

    def __post_init__(self):
        if self.start > self.end:
            # Need to swap - store original values first
            start, end = self.start, self.end
            object.__setattr__(self, "start", end)
            object.__setattr__(self, "end", start)

    @classmethod
    def from_length(cls, start: int, length: int) -> Interval:
        """Create interval from start point and length."""
        return cls(start, start + length - 1)

    @property
    def length(self) -> int:
        """Number of integer values in the interval."""
        return self.end - self.start + 1

    def __len__(self) -> int:
        return self.length

    def __bool__(self) -> bool:
        return self.start <= self.end

    def __contains__(self, item) -> bool:
        """Check if value or interval is contained."""
        if isinstance(item, Interval):
            return self.start <= item.start and item.end <= self.end
        return self.start <= item <= self.end

    def __iter__(self):
        """Iterate through all integer values in the interval."""
        yield from range(self.start, self.end + 1)

    def __and__(self, other: Interval) -> Interval | None:
        """Intersection operator: a & b"""
        return self.intersection(other)

    def __or__(self, other: Interval) -> Interval | None:
        """Union operator: a | b (returns None if not adjacent/overlapping)"""
        return self.union(other)

    def __sub__(self, other: Interval) -> list[Interval]:
        """Difference operator: a - b"""
        return self.difference(other)

    def __add__(self, offset: int) -> Interval:
        """Translate interval by offset: a + 5"""
        return Interval(self.start + offset, self.end + offset)

    def overlaps(self, other: Interval) -> bool:
        """Check if intervals overlap (share at least one value)."""
        return self.start <= other.end and other.start <= self.end

    def adjacent(self, other: Interval) -> bool:
        """Check if intervals are adjacent (touching but not overlapping)."""
        return self.end + 1 == other.start or other.end + 1 == self.start

    def intersection(self, other: Interval) -> Interval | None:
        """Return overlapping interval or None if no overlap."""
        if not self.overlaps(other):
            return None
        return Interval(max(self.start, other.start), min(self.end, other.end))

    def union(self, other: Interval) -> Interval | None:
        """Merge intervals if overlapping or adjacent, else None."""
        if not self.overlaps(other) and not self.adjacent(other):
            return None
        return Interval(min(self.start, other.start), max(self.end, other.end))

    def difference(self, other: Interval) -> list[Interval]:
        """Return parts of self not covered by other (0, 1, or 2 intervals)."""
        if not self.overlaps(other):
            return [self]
        result = []
        if self.start < other.start:
            result.append(Interval(self.start, other.start - 1))
        if self.end > other.end:
            result.append(Interval(other.end + 1, self.end))
        return result

    def split_at(self, value: int) -> tuple[Interval | None, Interval | None]:
        """Split interval at value, returning (left, right) parts."""
        if value <= self.start:
            return None, self
        if value > self.end:
            return self, None
        return Interval(self.start, value - 1), Interval(value, self.end)

    def clamp(self, value: int) -> int:
        """Clamp value to interval bounds."""
        return max(self.start, min(self.end, value))

    def expand(self, amount: int) -> Interval:
        """Grow interval by amount on both sides."""
        return Interval(self.start - amount, self.end + amount)

    def shift(self, offset: int) -> Interval:
        """Translate interval by offset (alias for __add__)."""
        return self + offset
