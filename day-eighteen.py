import functools
import math
from enum import Enum

def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, list) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x

test_data = [
    "[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]\n", "[[[5,[2,8]],4],[5,[[9,9],0]]]\n",
    "[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]\n", "[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]\n",
    "[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]\n", "[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]\n",
    "[[[[5,4],[7,7]],8],[[8,3],8]]\n", "[[9,3],[[9,9],[6,[4,9]]]]\n", "[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]\n",
    "[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]\n"
]

magnitude_checks = [{
    "pairs": "[[9,1],[1,9]]",
    "magnitude": 129
}, {
    "pairs": "[[1,2],[[3,4],5]]",
    "magnitude": 143
}, {
    "pairs": "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",
    "magnitude": 1384
}, {
    "pairs": "[[[[1,1],[2,2]],[3,3]],[4,4]]",
    "magnitude": 445
}, {
    "pairs": "[[[[3,0],[5,3]],[4,4]],[5,5]]",
    "magnitude": 791
}, {
    "pairs": "[[[[5,0],[7,4]],[5,5]],[6,6]]",
    "magnitude": 1137
}, {
    "pairs": "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
    "magnitude": 3488
}]


def calculate_magnitude(value):

    if (isinstance(value, list)):
        return (3 * calculate_magnitude(value[0])) + (2 * calculate_magnitude(value[1]))

    return value


# To explode a pair, the pair's left value is added to the first regular number
# to the left of the exploding pair (if any), and the pair's right value is added
# to the first regular number to the right of the exploding pair (if any).
# Exploding pairs will always consist of two regular numbers. Then, the entire
# exploding pair is replaced with the regular number 0.

explode_tests = [([[[[[9, 8], 1], 2], 3], 4], [[[[0, 9], 2], 3], 4]), ([7, [6, [5, [4, [3,
                                                                                        2]]]]], [7, [6, [5, [7, 0]]]]),
                 ([[6, [5, [4, [3, 2]]]], 1], [[6, [5, [7, 0]]], 3]),
                 ([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]], [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]),
                 ([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]], [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])]

next_left_right_tests = [([[[[[9, 8], 99], 2], 3], 4], (None, 99)), ([7, [6, [5, [99, [3, 2]]]]], (99, None)),
                         ([[6, [5, [99, [3, 2]]]], 98], (99, 98))]


class Node:
    def __init__(self, value, depth, parent):
        self.left = None
        self.right = None
        self.value = value
        self.depth = depth
        self.parent = parent

    @property
    def leaf(self):
        return self.value != None

    def next_left_leaf(self):
        assert self.leaf
        return None

    def __str__(self):
        if (self.value is None):
            return "[" + str(self.left) + "," + str(self.right) + "]"
        return str(self.value)


def build_tree(value, depth=0, parent=None):

    assert not isinstance(value, Node)

    if (not isinstance(value, list)):
        return Node(value, depth, parent)

    node = Node(None, depth, parent)
    left_value = value[0]
    right_value = value[1]
    node.left = build_tree(left_value, depth + 1, node)
    node.right = build_tree(right_value, depth + 1, node)
    return node


def node_to_explode(node):
    """
    Traverse the tree looking for a node with depth 4 with two leaf node children.
    """
    if (node.value is not None):
        return None
    if (node.depth == 4 and node.left.leaf and node.right.leaf):
        return node
    return node_to_explode(node.left) or node_to_explode(node.right)


def traverse(node, leaf_nodes=[]):

    if (node.leaf):
        leaf_nodes.append(node)
        return

    traverse(node.left, leaf_nodes)
    traverse(node.right, leaf_nodes)

    return leaf_nodes


def next_leaves(tree, node):
    assert node.left.leaf
    assert node.right.leaf
    nodes = traverse(tree, [])
    for i, current_node in enumerate(nodes):
        if current_node == node.left:
            return (nodes[i - 1] if i > 0 else None, nodes[i + 2] if i < len(nodes) - 2 else None)


for test in next_left_right_tests:
    tree = build_tree(test[0])
    test_next_leaves = next_leaves(tree, node_to_explode(tree))
    assert (test_next_leaves[0] and test_next_leaves[0].value, test_next_leaves[1]
            and test_next_leaves[1].value) == test[1], "This test failed %s -> %s" % (str(test), test_next_leaves)


def explode(tree):
    node = node_to_explode(tree)
    assert node is not None
    next_left, next_right = next_leaves(tree, node)

    def update_next_leaf(leaf_node, value):
        if leaf_node is not None:
            assert leaf_node.leaf
            leaf_node.value += value

    update_next_leaf(next_left, node.left.value)
    update_next_leaf(next_right, node.right.value)
    node.left = None
    node.right = None
    node.value = 0
    return tree


for test in explode_tests:
    try:
        exploded_tree = explode(build_tree(test[0]))
    except:
        print(test)
        raise
    assert eval(str(exploded_tree)) == test[1], "This test failed %s -> %s" % (str(test), str(exploded_tree))


def node_to_split(node):
    nodes = [x for x in traverse(node, []) if x.value >= 10]
    if (nodes):
        return nodes[0]
    return None


def split(tree):
    node = node_to_split(tree)
    assert node is not None
    node.left = build_tree(math.floor(node.value / 2), node.depth + 1, node)
    node.right = build_tree(math.ceil(node.value / 2), node.depth + 1, node)
    node.value = None
    return tree


# If any pair is nested inside four pairs, the leftmost such pair explodes.
# If any regular number is 10 or greater, the leftmost such regular number splits.
# Once no action in the above list applies, the snailfish number is reduced.


def reduce(tree):
    node = node_to_explode(tree)
    if (node is not None):
        exploded_tree = explode(tree)
        return reduce(exploded_tree)
    node = node_to_split(tree)
    if (node is not None):
        split_tree = split(tree)
        return reduce(split_tree)
    return tree


def add_arrays(array_one, array_two):
    return build_tree([array_one, array_two])


def add_then_reduce(array_one, array_two):
    try:
        reduced_tree = reduce(build_tree([array_one, array_two]))
    except:
        print(array_one)
        print(array_two)
        raise
    return eval(str(reduced_tree))


reduce_checks = [([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]], [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]])]

for test in reduce_checks:
    try:
        reduced = reduce(build_tree(test[0]))
        assert eval(str(reduced)) == test[1], "Expected %s, Reduced %s" % (reduced, test[1])
    except:
        raise

for check in magnitude_checks:
    assert calculate_magnitude(eval(check["pairs"])) == check["magnitude"]

f = open('day-eighteen-input.txt')
real_data = [eval(line.strip()) for line in f.readlines()]
f.close()

# Part One
add_then_reduce_tests = [([[1, 1], [2, 2], [3, 3], [4, 4]], [[[[1, 1], [2, 2]], [3, 3]], [4, 4]]),
                         ([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]], [[[[5, 0], [7, 4]], [5, 5]], [6, 6]]),
                         ([[[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9,
                                                                       5]]], [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]],
                           [[2, [[0, 8], [3, 4]]], [[[6, 7], 1], [7, [1, 6]]]],
                           [[[[2, 4], 7], [6, [0, 5]]], [[[6, 8], [2, 8]], [[2, 1], [4,
                                                                                     5]]]], [7, [5, [[3, 8], [1, 4]]]],
                           [[2, [2, 2]], [8, [8, 1]]], [2, 9], [1, [[[9, 3], 9], [[9, 0], [0, 7]]]],
                           [[[5, [7, 4]], 7], 1], [[[[4, 2], 2], 6], [8, 7]]], [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]],
                                                                                [[[0, 7], [6, 6]], [8, 7]]])]
for test in add_then_reduce_tests:
    final_pair_tree = functools.reduce(lambda a, b: add_then_reduce(a, b), test[0])
    assert test[1] == eval(str(final_pair_tree))

final_pair_tree = functools.reduce(lambda a,b: add_then_reduce(a,b), real_data)
print(calculate_magnitude(final_pair_tree))

# Part Two
print(max(flatten([[calculate_magnitude(add_then_reduce(a,b)) for a in real_data] for b in real_data])))
