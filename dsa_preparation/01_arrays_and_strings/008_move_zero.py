# Problem: Move all zeros to the end of array while maintaining the relative order of non-zero elements
# Input: [0,1,0,3,12]
# Output: [1,3,12,0,0]


def moveZeroes(nums):
    non_zero_pos = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[non_zero_pos], nums[i] = nums[i], nums[non_zero_pos]
            non_zero_pos += 1
    return nums


# Test cases
test_cases = [
    ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),
    ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
    ([0, 0, 1, 0, 0, 2, 3, 0, 0, 4], [1, 2, 3, 4, 0, 0, 0, 0, 0, 0]),
]

for nums, expected in test_cases:
    nums_copy = nums.copy()
    assert moveZeroes(nums_copy) == expected
