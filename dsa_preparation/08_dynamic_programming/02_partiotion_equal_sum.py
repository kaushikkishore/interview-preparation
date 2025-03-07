"""
https://leetcode.com/problems/partition-equal-subset-sum/description/

416. Partition Equal Subset Sum
Medium
Topics
Companies
Given an integer array nums, return true if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or false otherwise.



Example 1:

Input: nums = [1,5,11,5]
Output: true
Explanation: The array can be partitioned as [1, 5, 5] and [11].
Example 2:

Input: nums = [1,2,3,5]
Output: false
Explanation: The array cannot be partitioned into equal sum subsets.


Building a decision tree will help us to understand the problem.
"""

from typing import List


"""
Problem with this approach is its taking a lot of memory. 
"""

# class Solution:
#     def canPartition(self, nums: List[int]) -> bool:
#         dp = {}

#         total = sum(nums) / 2

#         def backtrack(i, total):
#             if total == 0:
#                 return True
#             if i == len(nums):
#                 return False

#             dp[(i, total)] = backtrack(i + 1, total - nums[i]) or backtrack(
#                 i + 1, total
#             )
#             return dp[(i, total)]

#         return backtrack(0, total)


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        if sum(nums) % 2 != 0:
            return False

        total = sum(nums) // 2
        dp = set()
        dp.add(0)

        for n in nums:
            next_dp = dp.copy()
            for t in dp:
                next_dp.add(t + n)
            dp = next_dp

        return total in dp


if __name__ == "__main__":
    nums = [1, 5, 11, 5]
    print(Solution().canPartition(nums))
