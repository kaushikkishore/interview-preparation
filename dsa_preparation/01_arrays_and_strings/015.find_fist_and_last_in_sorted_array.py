from typing import List


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        # Initialize pointers
        left = 0
        last_occurance = -1

        # Iterate through array with index and value
        for right, item in enumerate(nums):
            # When target is found
            if item == target:
                left = right  # Mark the first occurrence
                last_occurance = right  # Initialize last occurrence

                # Keep moving forward while we find the target
                while len(nums) > left and nums[left] == target:
                    last_occurance += 1
                    left += 1

                # Return [first occurrence, last occurrence]
                return [right, last_occurance]

        # If target not found, return [-1, -1]
        return [-1, -1]


# Test case
Solution().searchRange([5, 7, 7, 8, 8, 10], 8)
