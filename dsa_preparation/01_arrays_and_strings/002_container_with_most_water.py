"""
Problem: Container With Most Water
--------------------------------
Given n non-negative integers representing heights of walls, find two lines that
together with x-axis forms a container that holds the most water.

Approach Explanation:
1. We need to find two vertical lines and the x-axis that form a container holding maximum water
2. The amount of water is determined by:
   - Width: distance between the two lines (indices)
   - Height: minimum height of the two lines (can't hold water higher than shorter line)
3. Area formula: min(height1, height2) * (index2 - index1)

Time Complexity Analysis:
- Brute Force: O(n²)
- Optimized (Two Pointer): O(n)

Space Complexity Analysis:
- Both solutions: O(1)
"""


def max_area_brute_force(height: list[int]) -> int:
    """
    Brute Force Solution
    Time: O(n²), Space: O(1)
    """
    max_water = 0
    n = len(height)

    for i in range(n):
        for j in range(i + 1, n):
            width = j - i
            water = width * min(height[i], height[j])
            max_water = max(max_water, water)

    return max_water


def max_area_optimized(height: list[int]) -> int:
    """
    Optimized Solution using Two Pointer Technique
    Time: O(n), Space: O(1)

    Logic:
    1. Start with widest container (using two pointers)
    2. Move the pointer with shorter height inward
    3. Update max_area if current area is larger
    """
    left, right = 0, len(height) - 1
    max_water = 0

    while left < right:
        width = right - left
        water = width * min(height[left], height[right])
        max_water = max(max_water, water)

        # Move the pointer with shorter height
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_water


# Test cases
def test_max_area():
    assert max_area_optimized([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert max_area_optimized([1, 1]) == 1
    assert max_area_optimized([4, 3, 2, 1, 4]) == 16
    print("All test cases passed!")


if __name__ == "__main__":
    test_max_area()
