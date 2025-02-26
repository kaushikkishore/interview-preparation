"""
Problem: Longest Substring Without Repeating Characters
----------------------------------------------------
Find the length of the longest substring without repeating characters.

Time Complexity Analysis:
- Brute Force: O(n³)
- Optimized (Sliding Window): O(n)

Space Complexity Analysis:
- Both solutions: O(min(m,n)) where m is the size of the character set
"""


def length_of_longest_substring_brute_force(s: str) -> int:
    """
    Brute Force Solution
    Time: O(n³), Space: O(min(m,n))
    """

    def check_unique(start: int, end: int) -> bool:
        char_set = set()
        for i in range(start, end + 1):
            if s[i] in char_set:
                return False
            char_set.add(s[i])
        return True

    n = len(s)
    max_len = 0

    for i in range(n):
        for j in range(i, n):
            if check_unique(i, j):
                max_len = max(max_len, j - i + 1)

    return max_len


def length_of_longest_substring_optimized(s: str) -> int:
    """
    Optimized Solution using Sliding Window
    Time: O(n), Space: O(min(m,n))

    Logic:
    1. Use sliding window with two pointers (left and right)
    2. Use hash map to store character positions
    3. When duplicate found, move left pointer to position after the first occurrence
    """
    # Dictionary to store the last seen position of each character
    char_map = {}  # char -> last position

    # Keep track of the maximum length found so far
    max_len = 0

    # Left pointer of the sliding window
    left = 0

    # Right pointer iterates through the string
    for right, char in enumerate(s):
        # If we find a duplicate character within our current window
        # (char exists in map AND its last position is >= left pointer)
        if char in char_map and char_map[char] >= left:
            # Move left pointer to the position right after the first occurrence
            # This effectively removes the first occurrence from our window
            left = char_map[char] + 1
        else:
            # No duplicate found, update max_len if current window is larger
            # Window size is (right - left + 1)
            max_len = max(max_len, right - left + 1)

        # Always update the last seen position of current character
        char_map[char] = right

    return max_len


# Test cases
def test_longest_substring():
    assert length_of_longest_substring_optimized("abcabcbb") == 3
    assert length_of_longest_substring_optimized("bbbbb") == 1
    assert length_of_longest_substring_optimized("pwwkew") == 3
    print("All test cases passed!")


if __name__ == "__main__":
    test_longest_substring()
