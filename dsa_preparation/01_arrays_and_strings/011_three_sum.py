"""
Problem: Given an array of integers, find all unique triplets that sum up to zero.
Input: [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]


"""


def threeSum(nums):
    nums.sort()  # Sort array to handle duplicates easily
    result = []

    for i in range(len(nums) - 2):
        # Skip duplicates for i
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        # Use two pointers for the remaining array
        left, right = i + 1, len(nums) - 1

        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]

            if current_sum == 0:
                result.append([nums[i], nums[left], nums[right]])

                # Skip duplicates for left pointer
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicates for right pointer
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1

                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1

    return result


# Test cases
test_cases = [
    ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),
    (
        [0, 0, 0, 0],
        [[0, 0, 0]],
    ),  # Fixed: When all elements are 0, [0,0,0] is a valid triplet
    ([-2, 0, 0, 2, 2], [[-2, 0, 2]]),
    (
        [-1, 0, 1, 2, -1, -4, -2, -3, 3, 0, 4],
        [
            [-4, 0, 4],
            [-4, 1, 3],
            [-3, -1, 4],
            [-3, 0, 3],
            [-3, 1, 2],
            [-2, -1, 3],
            [-2, 0, 2],
            [-1, -1, 2],
            [-1, 0, 1],
        ],
    ),
]

for nums, expected in test_cases:
    assert sorted(threeSum(nums)) == sorted(expected)

print("All test cases passed!")
