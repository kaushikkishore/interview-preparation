"""
https://neetcode.io/solutions/top-k-frequent-elements
https://leetcode.com/problems/top-k-frequent-elements/description/

347. Top K Frequent Elements - Explanation
Problem Link

Description
Given an integer array nums and an integer k, return the k most frequent elements within the array.

The test cases are generated such that the answer is always unique.

You may return the output in any order.

Example 1:

Input: nums = [1,2,2,3,3,3], k = 2

Output: [2,3]
Example 2:

Input: nums = [7,7], k = 1

Output: [7]
"""

from typing import List
import heapq


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = {}
        for n in nums:
            count[n] = 1 + count.get(n, 0)

        heap = []
        for key, value in count.items():
            heapq.heappush(heap, (value, key))
            if len(heap) > k:
                heapq.heappop(heap)

        return [heapq.heappop(heap)[1] for _ in range(k)]


print(Solution().topKFrequent([1, 2, 2, 3, 3, 3], 2))
