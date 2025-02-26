"""
Problem: Trapping Rain Water
--------------------------
Given n non-negative integers representing an elevation map where the width of each bar is 1,
compute how much water it can trap after raining.

Time Complexity Analysis:
- Brute Force: O(n²)
- Dynamic Programming: O(n)
- Two Pointer: O(n)

Space Complexity Analysis:
- Brute Force: O(1)
- Dynamic Programming: O(n)
- Two Pointer: O(1)
"""


def trap_brute_force(height: list[int]) -> int:
    """
    Brute Force Solution
    Time: O(n²), Space: O(1)

    For each element:
    1. Find maximum height to its left
    2. Find maximum height to its right
    3. The water trapped = min(left_max, right_max) - current_height
    """
    total_water = 0
    n = len(height)

    # Skip first and last element as they can't trap water
    for i in range(1, n - 1):
        left_max = max(height[:i])  # Maximum height to the left
        right_max = max(height[i + 1 :])  # Maximum height to the right

        # Water trapped at current position
        water = min(left_max, right_max) - height[i]
        if water > 0:
            total_water += water

    return total_water


def trap_dynamic_programming(height: list[int]) -> int:
    """
    Dynamic Programming Solution
    Time: O(n), Space: O(n)

    1. Precompute left and right maximum heights
    2. Use these to calculate water trapped at each position
    """
    if not height:
        return 0

    n = len(height)
    total_water = 0

    # Precompute left maximum heights
    left_max = [0] * n
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])

    # Precompute right maximum heights
    right_max = [0] * n
    right_max[-1] = height[-1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])

    # Calculate trapped water
    for i in range(n):
        water = min(left_max[i], right_max[i]) - height[i]
        total_water += water

    return total_water


def trap_two_pointer(height: list[int]) -> int:
    """
    Two Pointer Solution (Most Optimal)
    Time: O(n), Space: O(1)

    Logic:
    1. Use two pointers (left and right)
    2. Track maximum height seen from left and right
    3. Move the pointer from the side with smaller height
    4. Calculate water trapped at each step
    """
    if not height:
        return 0

    total_water = 0
    left, right = 0, len(height) - 1
    left_max = right_max = 0

    while left < right:
        # Update maximum heights
        left_max = max(left_max, height[left])
        right_max = max(right_max, height[right])

        # Move pointer from the side with smaller height
        if left_max < right_max:
            total_water += left_max - height[left]
            left += 1
        else:
            total_water += right_max - height[right]
            right -= 1

    return total_water


# Test cases
def test_trap():
    # Test case 1: Regular case
    assert trap_two_pointer([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6

    # Test case 2: No water can be trapped
    assert trap_two_pointer([4, 2, 3]) == 1

    # Test case 3: Empty array
    assert trap_two_pointer([]) == 0

    # Test case 4: Single element
    assert trap_two_pointer([1]) == 0

    print("All test cases passed!")


if __name__ == "__main__":
    test_trap()
