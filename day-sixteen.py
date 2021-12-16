import functools
from enum import Enum
from itertools import groupby

hex_bits_packet = "D2FE28"
binary_equivalent = "110100101111111000101000"
hex_bits_packet = "E20D41"

test_data = [("38006F45291200", "00111000000000000110111101000101001010010001001000000000"),
             ("EE00D40C823060", "11101110000000001101010000001100100000100011000001100000")]


def hex_to_binary_char_buffer(hex_char_buffer):
    return "".join([format(int(c, 16), "04b") for c in hex_char_buffer])


f = open('day-sixteen-input.txt')
real_data = f.readlines()[0].strip()
f.close()

for hex_char_buffer, binary_char_buffer in test_data:
    assert hex_to_binary_char_buffer(hex_char_buffer) == binary_char_buffer


def consume_chunk(binary_char_buffer, current_offset, expected_length):
    return current_offset + expected_length, binary_char_buffer[current_offset:current_offset + expected_length]


def consume_value(binary_char_buffer, current_offset, expected_length):
    current_offset, chunk = consume_chunk(binary_char_buffer, current_offset, expected_length)
    return current_offset, int(chunk, 2)


def consume_literal_packet(binary_char_buffer, current_offset, version):

    current_chunk = ""
    group_buffer = ""
    starting_offset = current_offset

    while not current_chunk or current_chunk[0] != "0":
        current_offset, current_chunk = consume_chunk(binary_char_buffer, current_offset, 5)
        group_buffer += current_chunk[1:]

    # we found the last chunk, so get the literal value
    _, literal_value = consume_value(group_buffer, 0, len(group_buffer))

    return current_offset, {"type_id": 4, "version": version, "value": literal_value}


def consume_operator_packet(binary_char_buffer, current_offset, version, type_id):

    current_offset, length_type_id = consume_value(binary_char_buffer, current_offset, 1)

    subpackets = []
    if (length_type_id == 0):
        current_offset, bit_offset_for_subpackets = consume_value(binary_char_buffer, current_offset, 15)
        starting_offset = current_offset
        while (current_offset < starting_offset + bit_offset_for_subpackets):
            current_offset, bit_length_subpackets = consume_packet(binary_char_buffer, current_offset)
            subpackets.append(bit_length_subpackets)

    if (length_type_id == 1):
        current_offset, number_of_subpackets = consume_value(binary_char_buffer, current_offset, 11)
        for subpacket_index in range(0, number_of_subpackets):
            current_offset, counted_subpackets = consume_packet(binary_char_buffer, current_offset)
            subpackets.append(counted_subpackets)

    assert type(subpackets) is list
    return current_offset, {"type": "operator", "version": version, "subpackets": subpackets, "type_id": type_id}


LITERAL_TYPE_ID = 4
SUM_PACKET_ID = 0
PRODUCT_PACKET_ID = 1
MIN_PACKET_ID = 2
MAX_PACKET_ID = 3
GREATER_THAN_PACKET_ID = 5
LESS_THAN_PACKET_ID = 6
EQUAL_PACKET_ID = 7


def consume_packet(binary_char_buffer, current_offset=0):

    current_offset, version = consume_value(binary_char_buffer, current_offset, 3)
    current_offset, type_id = consume_value(binary_char_buffer, current_offset, 3)

    if (type_id == LITERAL_TYPE_ID):
        return consume_literal_packet(binary_char_buffer, current_offset, version)

    return consume_operator_packet(binary_char_buffer, current_offset, version, type_id)


offset, test_literal = consume_packet("10010000010", 0)
assert test_literal['value'] == 2
offset, test_literal = consume_packet("110100101111111000101000", 0)
assert test_literal['value'] == 2021
offset, test_operator_bits = consume_packet("00111000000000000110111101000101001010010001001000000000", 0)
offset, test_operator_packets = consume_packet("11101110000000001101010000001100100000100011000001100000", 0)


def sum_versions(packet):
    return packet["version"] + sum(sum_versions(subpacket) for subpacket in packet.get("subpackets") or [])


def value_cmp(packet, fn):
    assert len(packet.get("subpackets")) == 2
    first_packet = packet.get("subpackets")[0]
    second_packet = packet.get("subpackets")[1]
    return 1 if fn(first_packet, second_packet) else 0


def value_greater_than(packet):
    return value_cmp(packet,
                     lambda first_packet, second_packet: value_packet(first_packet) > value_packet(second_packet))


def value_less_than(packet):
    return value_cmp(packet,
                     lambda first_packet, second_packet: value_packet(first_packet) < value_packet(second_packet))


def value_equal(packet):
    return value_cmp(packet,
                     lambda first_packet, second_packet: value_packet(first_packet) == value_packet(second_packet))


def value_packet(packet):

    print(packet)
    if (packet["type_id"] == SUM_PACKET_ID):
        return sum([value_packet(subpacket) for subpacket in packet.get("subpackets")])
    if (packet["type_id"] == PRODUCT_PACKET_ID):
        return functools.reduce(lambda value1, value2: value1 * value2,
                                [value_packet(subpacket) for subpacket in packet.get("subpackets")])
    if (packet["type_id"] == MIN_PACKET_ID):
        return min([value_packet(subpacket) for subpacket in packet.get("subpackets")])
    if (packet["type_id"] == MAX_PACKET_ID):
        return max([value_packet(subpacket) for subpacket in packet.get("subpackets")])
    if (packet["type_id"] == LITERAL_TYPE_ID):
        return packet["value"]
    if (packet["type_id"] == GREATER_THAN_PACKET_ID):
        return value_greater_than(packet)
    if (packet["type_id"] == LESS_THAN_PACKET_ID):
        return value_less_than(packet)
    if (packet["type_id"] == EQUAL_PACKET_ID):
        return value_equal(packet)

    assert False


offset, real_packets = consume_packet(hex_to_binary_char_buffer(real_data), 0)
sum_version = sum_versions(real_packets)
print(value_packet(real_packets))
