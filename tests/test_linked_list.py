from aoc.linked_list import ListNode, SinglyListNode


def check_list(node, expected_values):
    for expected in expected_values:
        assert node.val == expected
        node = node.next_node
    assert node is None


def test_singly():
    values = [-4, -1, 0, 3, 10]
    node = SinglyListNode.from_list(values)
    check_list(node, values)


def test_reverse_singly():
    values = [-4, -1, 0, 3, 10]
    node = SinglyListNode.from_list(reversed(values))
    new_head = node.reverse()
    check_list(new_head, values)


def test_iterator():
    values = [-4, -1, 0, 3, 10]
    node = ListNode.from_list(values)
    for i, v in enumerate(node):
        assert v == values[i]


def test_singly_iterator():
    values = [-4, -1, 0, 3, 10]
    node = SinglyListNode.from_list(values)
    for i, v in enumerate(node):
        assert v == values[i]
