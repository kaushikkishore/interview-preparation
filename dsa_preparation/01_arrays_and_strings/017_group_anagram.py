# https://neetcode.io/solutions/group-anagrams
"""
Description
Given an array of strings strs, group all anagrams together into sublists. You may return the output in any order.

An anagram is a string that contains the exact same characters as another string, but the order of the characters can be different.

Example 1:

Input: strs = ["act","pots","tops","cat","stop","hat"]

Output: [["hat"],["act", "cat"],["stop", "pots", "tops"]]
Example 2:

Input: strs = ["x"]

Output: [["x"]]
Example 3:

Input: strs = [""]

Output: [[""]]


"""

from typing import List
from collections import defaultdict


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        result = defaultdict(list)
        for s in strs:
            count = [0] * 26
            for c in s:
                count[ord(c) - ord("a")] += 1
            result[tuple(count)].append(s)
        return list(result.values())


def test_group_anagrams():
    # Test case 1: Multiple anagram groups
    strs1 = ["act", "pots", "tops", "cat", "stop", "hat"]
    result1 = Solution().groupAnagrams(strs1)
    # Sort inner lists and outer list for consistent comparison
    result1 = [sorted(group) for group in result1]
    result1.sort(key=lambda x: x[0])
    assert result1 == [["act", "cat"], ["hat"], ["pots", "stop", "tops"]]

    # Test case 2: Single character
    strs2 = ["x"]
    result2 = Solution().groupAnagrams(strs2)
    assert result2 == [["x"]]

    # Test case 3: Empty string
    strs3 = [""]
    result3 = Solution().groupAnagrams(strs3)
    assert result3 == [[""]]

    # Test case 4: No anagrams
    strs4 = ["dog", "cat", "pig"]
    result4 = Solution().groupAnagrams(strs4)
    result4 = [sorted(group) for group in result4]
    result4.sort(key=lambda x: x[0])
    assert result4 == [["cat"], ["dog"], ["pig"]]

    print("All test cases passed!")


if __name__ == "__main__":
    test_group_anagrams()
