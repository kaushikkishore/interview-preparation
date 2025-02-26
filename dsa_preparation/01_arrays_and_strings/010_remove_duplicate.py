"""
Problem: Given a sorted array nums, remove the duplicates in-place such that each element appears only once and returns the new length.
Do not allocate extra space for another array; you must do this by modifying the input array in-place with O(1) extra memory.

Input: [1,1,2]
Output: 2, nums = [1,2]


"""


def removeDuplicates(nums):
    if not nums:
        return 0

    write_pointer = 1
    for read_pointer in range(1, len(nums)):
        if nums[read_pointer] != nums[read_pointer - 1]:
            nums[write_pointer] = nums[read_pointer]
            write_pointer += 1

    return write_pointer


# Test cases
test_cases = [
    ([1, 1, 2], 2, [1, 2]),
    ([0, 0, 1, 1, 1, 2, 2, 3, 3, 4], 5, [0, 1, 2, 3, 4]),
    ([1, 2, 3, 4, 5], 5, [1, 2, 3, 4, 5]),
    ([1, 1, 1, 1, 1], 1, [1]),
    ([], 0, []),
]

for nums, expected_length, expected_nums in test_cases:
    nums_copy = nums.copy()
    assert removeDuplicates(nums_copy) == expected_length
    assert nums_copy[:expected_length] == expected_nums

print("All test cases passed!")
