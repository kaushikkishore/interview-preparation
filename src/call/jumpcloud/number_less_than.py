def max_digit_sum_less_than(n_str):
    # Calculate digit sum
    def digit_sum(s):
        return sum(int(d) for d in s)

    # Convert string to array of digits
    digits = list(n_str)
    length = len(digits)

    # If single digit, just decrease it
    if length == 1:
        return str(int(n_str) - 1) if n_str != "1" else "0"

    # Decrease first digit by 1
    result = [str(int(digits[0]) - 1)]

    # Fill rest with 9s
    result.extend(["9"] * (length - 1))

    # Join and remove leading zeros
    result_str = "".join(result).lstrip("0")
    return result_str if result_str else "0"


# Test cases
test_cases = [
    "123",
    "99",
    "100",
    "9",
    "500",
    "12345678901234567890",
    "55555555555555555555",
]

for num in test_cases:
    result = max_digit_sum_less_than(num)
    digit_sum = sum(int(d) for d in result)
    print(f"Input: {num}")
    print(f"Result: {result}")
    print(f"Digit Sum: {digit_sum}")
    print(f"Verification: {result < num}")
    print()
