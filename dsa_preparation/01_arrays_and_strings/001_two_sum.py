"""
Problem: Two Sum
---------------
Given an array of integers nums and an integer target, return indices of the two numbers that add up to target.

Time Complexity Analysis:
- Brute Force: O(n²)
- Optimized (Hash Map): O(n)

Space Complexity Analysis:
- Brute Force: O(1)
- Optimized (Hash Map): O(n)
"""


def two_sum_brute_force(nums: list[int], target: int) -> list[int]:
    """
    Brute Force Solution
    Time: O(n²), Space: O(1)
    """
    # Approach:
    # 1. Use nested loops to check every possible pair of numbers
    # 2. Outer loop (i) selects the first number
    # 3. Inner loop (j) checks all numbers after i
    # 4. If any pair sums to target, return their indices
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


def two_sum_optimized(nums: list[int], target: int) -> list[int]:
    """
    Optimized Solution using Hash Map
    Time: O(n), Space: O(n)
    """
    # Approach:
    # 1. Use a hash map to store numbers we've seen (value -> index)
    # 2. For each number (num), calculate its complement (target - num)
    # 3. If complement exists in hash map, we found our pair
    # 4. If not, add current number and its index to hash map
    # 5. Continue until pair is found or array is exhausted
    num_map = {}  # val -> index

    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i

    return []


# Test cases
def test_two_sum():
    assert two_sum_optimized([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum_optimized([3, 2, 4], 6) == [1, 2]
    assert two_sum_optimized([3, 3], 6) == [0, 1]
    print("All test cases passed!")


if __name__ == "__main__":
    test_two_sum()
