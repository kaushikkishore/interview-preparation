"""
Problem: Given a sorted array of integers, return an array of the squares of each number sorted in non-decreasing order.
Input: [-4, -1, 0, 3, 10]
Output: [0, 1, 9, 16, 100]


Let's break down why this is an efficient in-place solution:

We use two pointers (left and right)
We compare absolute values since squaring changes negative numbers
We build the result from right to left since larger squares will be at the end
Only O(1) extra space is used for variables (excluding the result array)

"""


def sortedSquares(nums):
    n = len(nums)
    result = [0] * n
    left, right = 0, n - 1
    for i in range(n - 1, -1, -1):
        if abs(nums[left]) > abs(nums[right]):
            result[i] = nums[left] * nums[left]
            left += 1
        else:
            result[i] = nums[right] * nums[right]
            right -= 1
    return result


# Test cases
test_cases = [
    ([-4, -1, 0, 3, 10], [0, 1, 9, 16, 100]),
    ([-7, -3, 2, 3, 11], [4, 9, 9, 49, 121]),
    ([-5, -3, -2, -1], [1, 4, 9, 25]),
    ([1, 2, 3, 4], [1, 4, 9, 16]),
    ([-1, 2, 2], [1, 4, 4]),
]

for nums, expected in test_cases:
    assert sortedSquares(nums) == expected

print("All test cases passed!")
