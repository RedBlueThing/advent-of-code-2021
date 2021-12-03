import functools

test_data = ["11110", "10110", "10111", "10101", "01111", "00111", "11100", "10000", "11001", "00010", "01010"]
expected_gamma_rate = 22
expected_epsilon_rate = 9

def power_consumption(gamma_rate, epsilon_rate):
    return gamma_rate * epsilon_rate

def integer_data(test_data):
    return [int(x, 2) for x in test_data]

def bit_at(data, index):
    return((data & (1 << index)) >> index)

def gamma_test_func(bits_at_position):
    return (sum(bits_at_position) > len(bits_at_position) / 2)

def epsilon_test_func(bits_at_position):
    return not gamma_test_func(bits_at_position)

def bits_for_rate(test_func, data, bits):
    return [1 if test_func(x) else 0 for x in [[bit_at(datum, index) for datum in data] for index in range(0,bits)]]

gamma_rate = int("".join([str(x) for x in list(reversed(bits_for_rate(gamma_test_func, integer_data(test_data), 5)))]), 2)
epsilon_rate = int("".join([str(x) for x in list(reversed(bits_for_rate(epsilon_test_func, integer_data(test_data), 5)))]), 2)

print(gamma_rate == expected_gamma_rate)
print(epsilon_rate == expected_epsilon_rate)

f = open('day-three-input.txt')
raw_data = f.readlines()
data = integer_data(raw_data)
bit_length = len(raw_data[0].strip())
# bit_length = max([int.bit_length(x) for x in data])
gamma_rate = int("".join([str(x) for x in list(reversed(bits_for_rate(gamma_test_func, data, bit_length)))]), 2)
epsilon_rate = int("".join([str(x) for x in list(reversed(bits_for_rate(epsilon_test_func, data, bit_length)))]), 2)
print(power_consumption(gamma_rate, epsilon_rate))
f.close()

