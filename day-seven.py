import functools
import pygame
import threading

test_data = "16,1,2,0,4,2,7,1,2,14"
part_one_expected_fuel_cost = 37
part_two_expected_fuel_cost = 168

f = open('day-seven-input.txt')
real_data = f.readlines()[0]
f.close()


def positions_for_crab_submarines(data):
    return [int(x) for x in data.split(",")]


def fuel_cost_part_one(crab_positions, target_position):
    return sum([abs(position - target_position) for position in crab_positions])


def triangular_numbers(total_steps):
    # Triangular numbers!!!!! 6+5+4+3+2+1 == 6 * (6 + 1) / 2
    return total_steps * (total_steps + 1) / 2


def fuel_cost_part_two(crab_positions, target_position):
    return sum([triangular_numbers(abs(position - target_position)) for position in crab_positions])


def calculate_cheapest_fuel_cost(crab_positions, fuel_cost_fn):
    average_position = sum(crab_positions) / len(crab_positions)
    return min([fuel_cost_fn(crab_positions, target_position) for target_position in range(0, len(crab_positions))])


print("Part One - Test Data Check")
print(
    calculate_cheapest_fuel_cost(positions_for_crab_submarines(test_data), fuel_cost_part_one) ==
    part_one_expected_fuel_cost)
print("Part One - Real Data")
print(calculate_cheapest_fuel_cost(positions_for_crab_submarines(real_data), fuel_cost_part_one))

print("Part Two - Test Data Check")
print(
    calculate_cheapest_fuel_cost(positions_for_crab_submarines(test_data), fuel_cost_part_two) ==
    part_two_expected_fuel_cost)

print("Part Two - Real Data")
print(calculate_cheapest_fuel_cost(positions_for_crab_submarines(real_data), fuel_cost_part_two))
