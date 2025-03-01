def factorial(n):
    # Initialize result array with 1
    result = [1]

    # Calculate factorial from 2 to n
    for i in range(2, n + 1):
        # Multiply current number with previous result
        carry = 0

        # Multiply each digit and handle carry
        for j in range(len(result)):
            product = result[j] * i + carry
            result[j] = product % 10  # Keep the last digit
            carry = product // 10  # Calculate carry for next position

        # Add remaining carry digits to result
        while carry:
            result.append(carry % 10)
            carry //= 10

    # Return number in correct order (reverse array)
    return "".join(map(str, result[::-1]))


# Test cases
test_numbers = [5, 10, 20, 50, 100]
for n in test_numbers:
    print(f"{n}! = {factorial(n)}")
