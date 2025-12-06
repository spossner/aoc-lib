from __future__ import annotations

import heapq
from collections import deque
from collections.abc import Callable, Iterator

from .point import ALL_ADJACENTS, DIRECT_ADJACENTS, Point


class Grid:
    """2D grid with Point-based access."""

    def __init__(self, data: list[str] | list[list[str]]):
        """Create grid from list of strings or list of lists."""
        if not data:
            self._data = []
        elif isinstance(data[0], str):
            self._data = [list(row) for row in data]
        else:
            self._data = [list(row) for row in data]

    @classmethod
    def parse(cls, text: str) -> Grid:
        """Parse multiline string into Grid."""
        lines = text.strip().split("\n")
        return cls(lines)

    @classmethod
    def create(cls, width: int, height: int, fill: str = ".") -> Grid:
        """Create empty grid with fill character."""
        data = [[fill] * width for _ in range(height)]
        return cls(data)

    @property
    def width(self) -> int:
        return len(self._data[0]) if self._data else 0

    @property
    def height(self) -> int:
        return len(self._data)

    def __getitem__(self, p: Point | tuple) -> str:
        return self._data[p[1]][p[0]]

    def __setitem__(self, p: Point | tuple, value: str):
        self._data[p[1]][p[0]] = value

    def __contains__(self, p: Point | tuple) -> bool:
        return 0 <= p[0] < self.width and 0 <= p[1] < self.height

    def get(self, p: Point | tuple, default: str | None = None) -> str | None:
        if p in self:
            return self[p]
        return default

    def __iter__(self) -> Iterator[Point]:
        for y in range(self.height):
            for x in range(self.width):
                yield Point(x, y)

    def items(self) -> Iterator[tuple[Point, str]]:
        for p in self:
            yield p, self[p]

    def rows(self) -> Iterator[str]:
        for row in self._data:
            yield "".join(row)

    def find(self, value: str) -> Point | None:
        for p, v in self.items():
            if v == value:
                return p
        return None

    def find_all(self, value: str) -> list[Point]:
        return [p for p, v in self.items() if v == value]

    def neighbors(self, p: Point | tuple, diagonal: bool = False) -> Iterator[Point]:
        adjacents = ALL_ADJACENTS if diagonal else DIRECT_ADJACENTS
        for dx, dy in adjacents:
            np = Point(p[0] + dx, p[1] + dy)
            if np in self:
                yield np

    def neighbor_values(
        self, p: Point | tuple, diagonal: bool = False
    ) -> Iterator[tuple[Point, str]]:
        for np in self.neighbors(p, diagonal):
            yield np, self[np]

    def flood_fill(
        self, start: Point | tuple, predicate: Callable[[str], bool] | None = None
    ) -> set[Point]:
        if predicate is None:
            start_value = self[start]

            def predicate(v):
                return v == start_value

        result = set()
        queue = deque([Point(*start) if not isinstance(start, Point) else start])

        while queue:
            p = queue.popleft()
            if p in result or p not in self:
                continue
            if not predicate(self[p]):
                continue
            result.add(p)
            for np in self.neighbors(p):
                if np not in result:
                    queue.append(np)

        return result

    def bfs(
        self,
        start: Point | tuple,
        goal: Point | tuple | Callable[[Point], bool],
        diagonal: bool = False,
        passable: Callable[[str], bool] | None = None,
    ) -> tuple[list[Point], int] | None:
        """
        BFS pathfinding. Returns (path, distance) or None if no path found.

        :param start: Starting point
        :param goal: Target point or predicate function
        :param diagonal: Include diagonal neighbors
        :param passable: Predicate to check if a cell is passable (default: not '#')
        """
        if passable is None:

            def passable(v):
                return v != "#"

        is_goal = goal if callable(goal) else lambda p: p[0] == goal[0] and p[1] == goal[1]
        start = Point(*start) if not isinstance(start, Point) else start

        queue = deque([([start], 0)])
        seen = {start}

        while queue:
            path, dist = queue.popleft()
            node = path[-1]

            if is_goal(node):
                return path, dist

            for neighbor in self.neighbors(node, diagonal):
                if neighbor in seen:
                    continue
                if not passable(self[neighbor]):
                    continue
                seen.add(neighbor)
                queue.append(([*path, neighbor], dist + 1))

        return None

    def dfs(
        self,
        start: Point | tuple,
        goal: Point | tuple | Callable[[Point], bool],
        diagonal: bool = False,
        passable: Callable[[str], bool] | None = None,
    ) -> int:
        """
        DFS to find longest path. Returns max distance or -1 if no path.

        :param start: Starting point
        :param goal: Target point or predicate function
        :param diagonal: Include diagonal neighbors
        :param passable: Predicate to check if a cell is passable (default: not '#')
        """
        if passable is None:

            def passable(v):
                return v != "#"

        is_goal = goal if callable(goal) else lambda p: p[0] == goal[0] and p[1] == goal[1]
        start = Point(*start) if not isinstance(start, Point) else start

        def _dfs(cur: Point, path_set: set[Point], total_dist: int, best: int) -> int:
            if is_goal(cur):
                return max(best, total_dist)

            for neighbor in self.neighbors(cur, diagonal):
                if neighbor in path_set:
                    continue
                if not passable(self[neighbor]):
                    continue
                path_set.add(neighbor)
                best = _dfs(neighbor, path_set, total_dist + 1, best)
                path_set.remove(neighbor)

            return best

        return _dfs(start, {start}, 0, -1)

    def dijkstra(
        self,
        start: Point | tuple,
        goal: Point | tuple | Callable[[Point], bool],
        cost: Callable[[Point, Point, str], int] | None = None,
        diagonal: bool = False,
        passable: Callable[[str], bool] | None = None,
    ) -> tuple[list[Point], int] | None:
        """
        Dijkstra pathfinding with optional cost function.

        :param start: Starting point
        :param goal: Target point or predicate function
        :param cost: Cost function(from_point, to_point, to_value) -> int. Default: 1
        :param diagonal: Include diagonal neighbors
        :param passable: Predicate to check if a cell is passable (default: not '#')
        :return: (path, total_cost) or None if no path
        """
        if passable is None:

            def passable(v):
                return v != "#"

        if cost is None:

            def cost(_from, _to, _val):
                return 1

        is_goal = goal if callable(goal) else lambda p: p[0] == goal[0] and p[1] == goal[1]
        start = Point(*start) if not isinstance(start, Point) else start

        heap = [(0, [start])]
        min_costs = {start: 0}

        while heap:
            total_dist, path = heapq.heappop(heap)
            node = path[-1]

            if is_goal(node):
                return path, total_dist

            for neighbor in self.neighbors(node, diagonal):
                if not passable(self[neighbor]):
                    continue
                edge_cost = cost(node, neighbor, self[neighbor])
                new_cost = total_dist + edge_cost

                if neighbor not in min_costs or new_cost < min_costs[neighbor]:
                    min_costs[neighbor] = new_cost
                    heapq.heappush(heap, (new_cost, [*path, neighbor]))

        return None

    def copy(self) -> Grid:
        return Grid([row[:] for row in self._data])

    def transpose(self) -> Grid:
        transposed = [list(row) for row in zip(*self._data)]
        return Grid(transposed)

    def __str__(self) -> str:
        return "\n".join(self.rows())

    def __repr__(self) -> str:
        return f"Grid({self.width}x{self.height})"
