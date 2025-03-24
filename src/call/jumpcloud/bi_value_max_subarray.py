"""
Bi-Valued Maximum Subarray

Problem:
We call an array bi-valued if it contains at most two different numbers.
Given an array A consisting of N integers, find the length of the longest bi-valued slice
(continuous fragment) in the array.

Examples:
1. Given A = [4, 2, 2, 4, 2], the function should return 5, because the whole array is bi-valued.
2. Given A = [1, 2, 3, 2], the function should return 3. The longest bi-valued slice is [2, 3, 2].
3. Given A = [0, 5, 4, 4, 5, 12], the function should return 4. The longest bi-valued slice is [5, 4, 4, 5].
4. Given A = [4, 4], the function should return 2.

Constraints:
- N is an integer within the range [1..100,000]
- Each element of array A is an integer within the range [-1,000,000,000..1,000,000,000]

Solution approach:
Uses a sliding window technique with a dictionary to track frequency
of elements in the current window.
"""


def solution(A):
    n = len(A)
    if n <= 2:
        return n  # If array has 0, 1, or 2 elements, the whole array is bi-valued

    max_length = 0
    left = 0
    distinct_values = {}

    for right in range(n):
        # Add the current element to our count
        if A[right] in distinct_values:
            distinct_values[A[right]] += 1
        else:
            distinct_values[A[right]] = 1

        # While we have more than 2 distinct values, shrink the window
        while len(distinct_values) > 2:
            distinct_values[A[left]] -= 1
            if distinct_values[A[left]] == 0:
                del distinct_values[A[left]]
            left += 1

        # Update max_length
        max_length = max(max_length, right - left + 1)

    return max_length


# Test cases
def test_solution():
    # Test case 1: Whole array is bi-valued
    assert solution([4, 2, 2, 4, 2]) == 5

    # Test case 2: Middle section is longest bi-valued slice
    assert solution([1, 2, 3, 2]) == 3

    # Test case 3: Middle section with specific pattern
    assert solution([0, 5, 4, 4, 5, 12]) == 4

    # Test case 4: Array with single value
    assert solution([4, 4]) == 2

    # Test case 5: Empty array
    assert solution([]) == 0

    # Test case 6: Single element array
    assert solution([7]) == 1

    # Test case 7: Array with all different values
    assert solution([1, 2, 3, 4, 5]) == 2

    # Test case 8: Large numbers within constraint range
    assert solution([1000000000, -1000000000, 1000000000]) == 3

    print("All test cases passed!")


# Uncomment to run the tests
if __name__ == "__main__":
    test_solution()
