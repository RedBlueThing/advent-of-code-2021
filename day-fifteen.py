import functools
from enum import Enum
from itertools import groupby


def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, list) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


test_data = [
    "1163751742\n", "1381373672\n", "2136511328\n", "3694931569\n", "7463417111\n", "1319128137\n", "1359912421\n",
    "3125421639\n", "1293138521\n", "2311944581\n"
]

expected_enlarged_test_data = [
    "11637517422274862853338597396444961841755517295286\n",
    "13813736722492484783351359589446246169155735727126\n",
    "21365113283247622439435873354154698446526571955763\n",
    "36949315694715142671582625378269373648937148475914\n",
    "74634171118574528222968563933317967414442817852555\n",
    "13191281372421239248353234135946434524615754563572\n",
    "13599124212461123532357223464346833457545794456865\n",
    "31254216394236532741534764385264587549637569865174\n",
    "12931385212314249632342535174345364628545647573965\n",
    "23119445813422155692453326671356443778246755488935\n",
    "22748628533385973964449618417555172952866628316397\n",
    "24924847833513595894462461691557357271266846838237\n",
    "32476224394358733541546984465265719557637682166874\n",
    "47151426715826253782693736489371484759148259586125\n",
    "85745282229685639333179674144428178525553928963666\n",
    "24212392483532341359464345246157545635726865674683\n",
    "24611235323572234643468334575457944568656815567976\n",
    "42365327415347643852645875496375698651748671976285\n",
    "23142496323425351743453646285456475739656758684176\n",
    "34221556924533266713564437782467554889357866599146\n",
    "33859739644496184175551729528666283163977739427418\n",
    "35135958944624616915573572712668468382377957949348\n",
    "43587335415469844652657195576376821668748793277985\n",
    "58262537826937364893714847591482595861259361697236\n",
    "96856393331796741444281785255539289636664139174777\n",
    "35323413594643452461575456357268656746837976785794\n",
    "35722346434683345754579445686568155679767926678187\n",
    "53476438526458754963756986517486719762859782187396\n",
    "34253517434536462854564757396567586841767869795287\n",
    "45332667135644377824675548893578665991468977611257\n",
    "44961841755517295286662831639777394274188841538529\n",
    "46246169155735727126684683823779579493488168151459\n",
    "54698446526571955763768216687487932779859814388196\n",
    "69373648937148475914825958612593616972361472718347\n",
    "17967414442817852555392896366641391747775241285888\n",
    "46434524615754563572686567468379767857948187896815\n",
    "46833457545794456865681556797679266781878137789298\n",
    "64587549637569865174867197628597821873961893298417\n",
    "45364628545647573965675868417678697952878971816398\n",
    "56443778246755488935786659914689776112579188722368\n",
    "55172952866628316397773942741888415385299952649631\n",
    "57357271266846838237795794934881681514599279262561\n",
    "65719557637682166874879327798598143881961925499217\n",
    "71484759148259586125936169723614727183472583829458\n",
    "28178525553928963666413917477752412858886352396999\n",
    "57545635726865674683797678579481878968159298917926\n",
    "57944568656815567976792667818781377892989248891319\n",
    "75698651748671976285978218739618932984172914319528\n",
    "56475739656758684176786979528789718163989182927419\n",
    "67554889357866599146897761125791887223681299833479\n"
]

expected_lowest_risk_path = [1, 1, 2, 1, 3, 6, 5, 1, 1, 1, 5, 1, 1, 3, 2, 3, 2, 1, 1]
expected_total_risk = 40
assert sum(expected_lowest_risk_path[1:]) == expected_total_risk


def show_riskmap(riskmap, width, height):
    for y in range(0, height):
        for x in range(0, width):
            index = (width * y) + x
            print("%d:%d " % (index, riskmap[index]), end="")
        print("")


def in_range(riskmap, cell_index):
    return cell_index >= 0 and cell_index < len(riskmap)


def is_first_cell_in_row(width, cell_index):
    return cell_index % width == 0


def top(riskmap, width, height, cell_index):
    offset_index = cell_index - width
    return offset_index if in_range(riskmap, offset_index) else None


def bottom(riskmap, width, height, cell_index):
    offset_index = cell_index + width
    return offset_index if in_range(riskmap, offset_index) else None


def left(riskmap, width, height, cell_index):
    offset_index = cell_index - 1 if not is_first_cell_in_row(width, cell_index) else -1
    return offset_index if in_range(riskmap, offset_index) else None


def right(riskmap, width, height, cell_index):
    offset_index = cell_index + 1 if not is_first_cell_in_row(width, cell_index + 1) else -1
    return offset_index if in_range(riskmap, offset_index) else None


def adjacent_cell_indicies(riskmap, width, height, cell_index):
    return [
        adjacent_cell_index for adjacent_cell_index in [
            top(riskmap, width, height, cell_index),
            bottom(riskmap, width, height, cell_index),
            left(riskmap, width, height, cell_index),
            right(riskmap, width, height, cell_index)
        ] if adjacent_cell_index is not None
    ]


def process_lines(lines):
    # have to account for the end of line in this data
    width = len(lines[0]) - 1
    height = len(lines)
    riskmap = list(flatten([[int(c) for c in line if c != '\n'] for line in lines]))
    return (riskmap, width, height)


def build_graph(riskmap, width, height):

    graph = {}
    for index in range(0, len(riskmap)):
        graph[index] = {
            "visited": False,
            "tentative_distance": float('inf') if index > 0 else 0,
            "weight": riskmap[index],
            "neighbors": adjacent_cell_indicies(riskmap, width, height, index)
        }

    return graph


def check(current, destination):
    assert not destination["visited"]
    destination["tentative_distance"] = min(current["tentative_distance"] + destination["weight"],
                                            destination["tentative_distance"])


def unvisited_neighbors(node, visited_set):
    return filter(lambda neighbor_index: neighbor_index not in visited_set, node["neighbors"])

def unvisited_nodes(graph):
    return sorted([(x, graph[x]["tentative_distance"]) for x in graph.keys() if not graph[x]["visited"]], key=lambda cmp: cmp[1])


def dijkstra(graph, current_index, destination_index, visited_set):

    if (current_index == destination_index):
        return graph[current_index]

    current = graph[current_index]
    for unvisited_destination_index in unvisited_neighbors(current, visited_set):
        check(current, graph[unvisited_destination_index])

    visited_set.add(current_index)
    current["visited"] = True

    next_current_index, next_current_tentative_distance = unvisited_nodes(graph)[0]

    return dijkstra(graph, next_current_index, destination_index, visited_set)


def dijkstra(graph, start_index, destination_index):

    visited_set = set()
    current_index = start_index

    while (current_index != destination_index):

        current = graph[current_index]
        for unvisited_destination_index in unvisited_neighbors(current, visited_set):
            check(current, graph[unvisited_destination_index])

        visited_set.add(current_index)
        current["visited"] = True

        current_index, next_current_tentative_distance = unvisited_nodes(graph)[0]

    return graph[current_index]

# def enlarge_cave_riskmap(riskmap, width_multiple=5, height_multiple=5):

#     for rows in range(0, width_multiple)
def enlarge_cave_riskmap(riskmap, width, height):
    return riskmap, width, height


riskmap, width, height = process_lines(test_data)
print(dijkstra(build_graph(riskmap, width, height), 0, len(riskmap) - 1))

# f = open('day-fifteen-input.txt')
# real_data = f.readlines()
# f.close()

# riskmap, width, height = process_lines(real_data)
# print(dijkstra(build_graph(riskmap, width, height), 0, len(riskmap) - 1))

expected_enlarged_riskmap, expected_enlarged_width, expected_enlarged_height = process_lines(expected_enlarged_test_data)

assert enlarge_cave_riskmap(riskmap, width, height) == (expected_enlarged_riskmap, expected_enlarged_width, expected_enlarged_height)
