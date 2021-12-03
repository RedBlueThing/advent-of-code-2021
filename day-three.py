import functools

test_data = ["00100", "11110", "10110", "10111", "10101", "01111", "00111", "11100", "10000", "11001", "00010", "01010"]
expected_gamma_rate = 22
expected_epsilon_rate = 9
expected_oxygen_generator_rating = 23
expected_co2_scrubber_rating = 10

def life_support_rating(oxygen_generator_rating, co2_scrubber_rating):
    return oxygen_generator_rating * co2_scrubber_rating

def power_consumption(gamma_rate, epsilon_rate):
    return gamma_rate * epsilon_rate

# Some tools
def integer_data(test_data):
    return [int(x, 2) for x in test_data]

def bit_at(data, position):
    return((data & (1 << position)) >> position)

def integer_for_bits(bits):
    return functools.reduce(lambda value1, value2: value1 | value2[1] << value2[0] , list(enumerate(bits)), 0)

# Functions for rate and rating calculations
def gamma_test_func(bits_at_position):
    return (sum(bits_at_position) > len(bits_at_position) / 2)

def epsilon_test_func(bits_at_position):
    return not gamma_test_func(bits_at_position)

def extract_rate_using_test(test_func, data, bits):
    return [1 if test_func(x) else 0 for x in [[bit_at(datum, position) for datum in data] for position in range(0,bits)]]

def oxygen_generator_test_func(datum, bits_at_position, position):
    most_common_bit = 1 if sum(bits_at_position) >= (len(bits_at_position) / 2.0) else 0
    return bit_at(datum, position) == most_common_bit

def co2_scrubber_test_func(datum, bits_at_position, position):
    least_common_bit = 1 if sum(bits_at_position) < (len(bits_at_position) / 2.0) else 0
    return bit_at(datum, position) == least_common_bit

def extract_rating_using_test(test_func, data, bits):
    filtered_data = data
    for index in range(0,bits):
        position = bits - (index + 1)
        bits_at_position = [bit_at(datum, position) for datum in filtered_data]
        filtered_data = filter(lambda datum: test_func(datum, bits_at_position, position), filtered_data)
        # Check if we finished before examining all the bit positions
        if (len(filtered_data) == 1):
            break
    assert len(filtered_data) == 1, "Filtered data is %s" % str(filtered_data)
    return filtered_data[0]

gamma_rate = integer_for_bits(extract_rate_using_test(gamma_test_func, integer_data(test_data), 5))
epsilon_rate = integer_for_bits(extract_rate_using_test(epsilon_test_func, integer_data(test_data), 5))
oxygen_generator_rating = extract_rating_using_test(oxygen_generator_test_func, integer_data(test_data), 5)
co2_scrubber_rating = extract_rating_using_test(co2_scrubber_test_func, integer_data(test_data), 5)

print(gamma_rate == expected_gamma_rate)
print(epsilon_rate == expected_epsilon_rate)
print(oxygen_generator_rating == expected_oxygen_generator_rating)
print(co2_scrubber_rating == expected_co2_scrubber_rating)

f = open('day-three-input.txt')
raw_data = f.readlines()
data = integer_data(raw_data)
bit_length = len(raw_data[0].strip())
# bit_length = max([int.bit_length(x) for x in data])
gamma_rate = integer_for_bits(extract_rate_using_test(gamma_test_func, data, bit_length))
epsilon_rate = integer_for_bits(extract_rate_using_test(epsilon_test_func, data, bit_length))
print(power_consumption(gamma_rate, epsilon_rate))
f.close()

f = open('day-three-input.txt')
raw_data = f.readlines()
data = integer_data(raw_data)
bit_length = len(raw_data[0].strip())
# bit_length = max([int.bit_length(x) for x in data])
oxygen_generator_rating = extract_rating_using_test(oxygen_generator_test_func, data, bit_length)
co2_scrubber_rating = extract_rating_using_test(co2_scrubber_test_func, data, bit_length)
print(life_support_rating(oxygen_generator_rating, co2_scrubber_rating))
f.close()
