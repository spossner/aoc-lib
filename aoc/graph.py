import heapq
from collections import deque, namedtuple, defaultdict
from itertools import chain

Edge = namedtuple("Edge", "child,dist", defaults=[1])


def edge_iter(edge):
    if type(edge) is Edge:
        yield edge
    elif type(edge) is tuple:
        assert len(edge) >= 1 and len(edge) <= 2  # assert it looks like an edge
        yield Edge(*edge)
    elif type(edge) is list or type(edge) is set:
        for e in edge:
            yield from edge_iter(e)
    else:
        yield Edge(edge)


def make_undirected(edges):
    new_edges = defaultdict(set)
    for k, v in edges.items():
        for edge in edge_iter(v):
            new_edges[k].add(edge)
            new_edges[edge.child].add(Edge(k, edge.dist))
    return new_edges


def node_set(edges):
    return set(map(lambda e: e.child, chain(*[edge_iter(e) for e in edges.values()]))).union(edges.keys())


def _bfs(edges, start, is_target, with_path=True):
    q = deque()
    q.append(([start] if with_path else start, 0))
    seen = {start}

    while q:
        path, total_dist = q.popleft()
        node = path[-1] if with_path else path
        if is_target(node):
            return (path, total_dist) if with_path else total_dist
        for child, dist in edge_iter(edges[node]):
            if child in seen:
                continue
            seen.add(node)
            q.append(([*path, child] if with_path else child, total_dist + dist))
    return None, -1 if with_path else -1


def _dfs(edges, cur, is_target, path_set=None, total_dist=0, best=0):
    if is_target(cur):
        return max(best, total_dist)
    if path_set is None:
        path_set = set()
    if cur in edges:  # has outgoing edges
        for child, dist in edge_iter(edges[cur]):
            if child not in path_set:
                path_set.add(child)
                best = _dfs(edges, child, is_target, path_set, total_dist + dist, best)
                path_set.remove(child)
    return best


def _dijkstra(edges, start, is_target, with_path=True):
    paths = []
    heapq.heappush(paths, (0, [start] if with_path else start))
    min_costs = {start: 0}
    while paths:
        total_dist, path = heapq.heappop(paths)
        node = path[-1] if with_path else path
        if is_target(node):
            return (path, total_dist) if with_path else total_dist
        if not node in edges:
            continue
        for child, dist in edge_iter(edges[node]):
            costs = total_dist + dist
            if child not in min_costs or costs < min_costs[child]:
                # found a (cheaper) path to child
                min_costs[child] = costs
                heapq.heappush(paths, (costs, [*path, child] if with_path else child))

    return None, -1 if with_path else -1


def bfs_all_nodes(edges, start):
    q = deque()
    q.append(start)
    seen = set()
    while q:
        node = q.popleft()
        if node in seen:
            continue
        seen.add(node)
        for child, _ in edge_iter(edges[node]):
            q.append(child)
    return seen


def bfs(edges, start, destination):
    is_target = destination if callable(destination) else lambda e: e == destination
    return _bfs(edges, start, is_target)


def bfs_length(edges, start, destination):
    is_target = destination if callable(destination) else lambda e: e == destination
    return _bfs(edges, start, is_target, with_path=False)


def dfs(edges, start, destination):
    is_target = destination if callable(destination) else lambda e: e == destination
    return _dfs(edges, start, is_target)


def dijkstra(edges, start, destination):
    is_target = destination if callable(destination) else lambda e: e == destination
    return _dijkstra(edges, start, is_target)


def dijkstra_length(edges, start, destination):
    is_target = destination if callable(destination) else lambda e: e == destination
    return _dijkstra(edges, start, is_target, with_path=False)


if __name__ == "__main__":
    edges = {
        'a': ['b'],
        'e': 'c',
        'c': ['a', 'b', ('d', 1.2)],
        'b': Edge('a', 1.4),
        'd': [Edge('a', 2), Edge('c'), 'f'],
        'f': [('c', 1.9), 'g'],
        'g': ('f',),
        0: 1,
        0: 2,
        2: [0, 1],
    }

    print(bfs(edges, 'c', lambda e: e.upper() >= 'E'))
    print(bfs_length(edges, 'c', 'g'))

    print(dfs(edges, 'c', 'g'))

    ed2 = {
        'a': [('b', 1), ('c', 3)],
        'b': ('c', 3),
    }

    print(dijkstra(ed2, 'a', 'c'))

    ed3 = {
        "A": [("B", 7), ("D", 5)],
        "B": [("C", 8), ("D", 9), ("E", 7)],
        "C": ("E", 5),
        "D": [("E", 15), ("F", 6), ],
        "E": [("F", 8), ("G", 9), ],
        "F": ("G", 11)
    }

    print(dijkstra(ed3, "A", "E"))
    print(dijkstra_length(ed3, "F", "G"))

    ed4 = {
        "a": [("b", 7), ("d", 14), ("c", 10)],
        "c": [("a", 9), ("f", 11)],
        "b": [("c", 10), ("f", 15)],
        "d": [("c", 2), ("e", 9)],
        "e": ("f", 6),
    }

    ed4_undirected = make_undirected(ed4)

    assert dijkstra_length(ed4_undirected, "a", "a") == 0
    assert dijkstra_length(ed4_undirected, "a", "b") == 7
    assert dijkstra_length(ed4_undirected, "a", "c") == 9
    assert dijkstra_length(ed4_undirected, "a", "d") == 11
    assert dijkstra_length(ed4_undirected, "a", "e") == 20
    assert dijkstra_length(ed4_undirected, "a", "f") == 20

    ed5 = {
        "a": [("b", 7), ("d", 14), ("c", 9), ],
        "b": [("c", 10), ("f", 15), ],
        "c": [("a", 9), ("b", 10), ("d", 2), ("f", 11), ],
        "d": [("c", 2), ("e", 9), ],
        "e": [("d", 9), ("f", 6), ],
        "f": [("b", 15), ("c", 11), ("e", 6), ],
    }

    assert dijkstra_length(ed5, "a", "a") == 0
    assert dijkstra_length(ed5, "a", "b") == 7
    assert dijkstra_length(ed5, "a", "c") == 9
    assert dijkstra_length(ed5, "a", "d") == 11
    assert dijkstra_length(ed5, "a", "e") == 20
    assert dijkstra_length(ed5, "a", "f") == 20
