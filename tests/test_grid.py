from aoc import Grid, Point


class TestGridCreation:
    def test_from_strings(self):
        grid = Grid(["abc", "def"])
        assert grid.width == 3
        assert grid.height == 2
        assert grid[Point(0, 0)] == "a"
        assert grid[Point(2, 1)] == "f"

    def test_from_list_of_lists(self):
        grid = Grid([["a", "b"], ["c", "d"]])
        assert grid.width == 2
        assert grid.height == 2
        assert grid[Point(1, 0)] == "b"

    def test_parse(self):
        text = "abc\ndef\nghi"
        grid = Grid.parse(text)
        assert grid.width == 3
        assert grid.height == 3
        assert grid[Point(1, 1)] == "e"

    def test_create_empty(self):
        grid = Grid.create(4, 3, ".")
        assert grid.width == 4
        assert grid.height == 3
        assert all(v == "." for _, v in grid.items())

    def test_create_with_fill(self):
        grid = Grid.create(2, 2, "#")
        assert grid[Point(0, 0)] == "#"
        assert grid[Point(1, 1)] == "#"


class TestGridAccess:
    def test_getitem_with_point(self):
        grid = Grid(["ab", "cd"])
        assert grid[Point(0, 0)] == "a"
        assert grid[Point(1, 0)] == "b"
        assert grid[Point(0, 1)] == "c"
        assert grid[Point(1, 1)] == "d"

    def test_getitem_with_tuple(self):
        grid = Grid(["ab", "cd"])
        assert grid[(0, 0)] == "a"
        assert grid[(1, 1)] == "d"

    def test_setitem(self):
        grid = Grid(["ab", "cd"])
        grid[Point(0, 0)] = "X"
        assert grid[Point(0, 0)] == "X"
        grid[(1, 1)] = "Y"
        assert grid[(1, 1)] == "Y"

    def test_contains(self):
        grid = Grid(["ab", "cd"])
        assert Point(0, 0) in grid
        assert Point(1, 1) in grid
        assert Point(2, 0) not in grid
        assert Point(0, 2) not in grid
        assert Point(-1, 0) not in grid
        assert (0, 0) in grid

    def test_get_with_default(self):
        grid = Grid(["ab", "cd"])
        assert grid.get(Point(0, 0)) == "a"
        assert grid.get(Point(5, 5)) is None
        assert grid.get(Point(5, 5), "X") == "X"


class TestGridIteration:
    def test_iter_points(self):
        grid = Grid(["ab", "cd"])
        points = list(grid)
        assert points == [Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)]

    def test_items(self):
        grid = Grid(["ab", "cd"])
        items = list(grid.items())
        assert items == [
            (Point(0, 0), "a"),
            (Point(1, 0), "b"),
            (Point(0, 1), "c"),
            (Point(1, 1), "d"),
        ]

    def test_rows(self):
        grid = Grid(["abc", "def"])
        rows = list(grid.rows())
        assert rows == ["abc", "def"]


class TestGridSearch:
    def test_find_existing(self):
        grid = Grid(["ab", "cd"])
        assert grid.find("c") == Point(0, 1)
        assert grid.find("a") == Point(0, 0)

    def test_find_not_found(self):
        grid = Grid(["ab", "cd"])
        assert grid.find("x") is None

    def test_find_all(self):
        grid = Grid(["aba", "bab"])
        result = grid.find_all("a")
        assert set(result) == {Point(0, 0), Point(2, 0), Point(1, 1)}

    def test_find_all_empty(self):
        grid = Grid(["ab", "cd"])
        assert grid.find_all("x") == []


class TestGridNeighbors:
    def test_neighbors_cardinal(self):
        grid = Grid(["abc", "def", "ghi"])
        neighbors = list(grid.neighbors(Point(1, 1)))
        assert set(neighbors) == {Point(1, 0), Point(2, 1), Point(1, 2), Point(0, 1)}

    def test_neighbors_diagonal(self):
        grid = Grid(["abc", "def", "ghi"])
        neighbors = list(grid.neighbors(Point(1, 1), diagonal=True))
        assert len(neighbors) == 8

    def test_neighbors_corner(self):
        grid = Grid(["abc", "def"])
        neighbors = list(grid.neighbors(Point(0, 0)))
        assert set(neighbors) == {Point(1, 0), Point(0, 1)}

    def test_neighbor_values(self):
        grid = Grid(["abc", "def"])
        values = list(grid.neighbor_values(Point(1, 0)))
        assert set(values) == {(Point(0, 0), "a"), (Point(2, 0), "c"), (Point(1, 1), "e")}


class TestGridFloodFill:
    def test_flood_fill_same_value(self):
        grid = Grid(["..#", "..#", "###"])
        result = grid.flood_fill(Point(0, 0))
        assert result == {Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)}

    def test_flood_fill_with_predicate(self):
        grid = Grid(["123", "456", "789"])
        result = grid.flood_fill(Point(0, 0), lambda v: int(v) < 5)
        # 1,2,3,4 are < 5; 5 is not, so Point(1,1) is not included
        assert result == {Point(0, 0), Point(1, 0), Point(2, 0), Point(0, 1)}


class TestGridBFS:
    def test_bfs_simple(self):
        grid = Grid(["...", "...", "..."])
        result = grid.bfs(Point(0, 0), Point(2, 2))
        assert result is not None
        path, dist = result
        assert path[0] == Point(0, 0)
        assert path[-1] == Point(2, 2)
        assert dist == 4

    def test_bfs_with_walls(self):
        grid = Grid(["...", ".#.", "..."])
        result = grid.bfs(Point(0, 0), Point(2, 2))
        assert result is not None
        path, dist = result
        assert Point(1, 1) not in path

    def test_bfs_no_path(self):
        grid = Grid(["..#", "###", "#.."])
        result = grid.bfs(Point(0, 0), Point(2, 2))
        assert result is None

    def test_bfs_with_predicate_goal(self):
        grid = Grid(["...E", "....", "...."])
        result = grid.bfs(Point(0, 0), lambda p: grid[p] == "E")
        assert result is not None
        path, dist = result
        assert grid[path[-1]] == "E"

    def test_bfs_with_custom_passable(self):
        grid = Grid(["S..", "XXX", "..E"])
        result = grid.bfs(Point(0, 0), Point(2, 2), passable=lambda v: v != "X")
        assert result is None


class TestGridDFS:
    def test_dfs_finds_path(self):
        grid = Grid(["...", "...", "..."])
        result = grid.dfs(Point(0, 0), Point(2, 2))
        assert result >= 4  # At least Manhattan distance

    def test_dfs_no_path(self):
        grid = Grid(["..#", "###", "#.."])
        result = grid.dfs(Point(0, 0), Point(2, 2))
        assert result == -1

    def test_dfs_longest_path(self):
        # DFS should find the longest path in a small grid
        grid = Grid(["...", "..."])
        result = grid.dfs(Point(0, 0), Point(2, 1))
        # Longest path visits all 6 cells: 5 steps
        assert result == 5


class TestGridDijkstra:
    def test_dijkstra_simple(self):
        grid = Grid(["...", "...", "..."])
        result = grid.dijkstra(Point(0, 0), Point(2, 2))
        assert result is not None
        path, cost = result
        assert path[0] == Point(0, 0)
        assert path[-1] == Point(2, 2)
        assert cost == 4

    def test_dijkstra_with_cost(self):
        # Cost based on cell value
        grid = Grid(["119", "191", "911"])
        # Each step costs the value of the destination cell
        result = grid.dijkstra(
            Point(0, 0),
            Point(2, 2),
            cost=lambda _from, _to, val: int(val),
            passable=lambda _: True,
        )
        assert result is not None
        path, total_cost = result
        assert path[-1] == Point(2, 2)
        # Optimal path should prefer 1s over 9s

    def test_dijkstra_no_path(self):
        grid = Grid(["..#", "###", "#.."])
        result = grid.dijkstra(Point(0, 0), Point(2, 2))
        assert result is None


class TestGridCopy:
    def test_copy_is_independent(self):
        grid = Grid(["ab", "cd"])
        copy = grid.copy()
        copy[Point(0, 0)] = "X"
        assert grid[Point(0, 0)] == "a"
        assert copy[Point(0, 0)] == "X"


class TestGridStr:
    def test_str(self):
        grid = Grid(["abc", "def"])
        assert str(grid) == "abc\ndef"

    def test_repr(self):
        grid = Grid(["abc", "def"])
        assert repr(grid) == "Grid(3x2)"
