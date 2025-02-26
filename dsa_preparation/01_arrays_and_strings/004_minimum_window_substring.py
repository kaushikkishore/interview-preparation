"""
Problem: Minimum Window Substring
-------------------------------
Given strings s and t, find the minimum window in s that contains all characters of t.

Time Complexity Analysis:
- Optimized (Sliding Window): O(|S| + |T|)
Space Complexity Analysis:
- O(|T|) for storing character frequencies
"""

from collections import Counter


def min_window(s: str, t: str) -> str:
    """
    Optimized Solution using Sliding Window and Counter

    Simple explanation:
    Imagine you're looking through a bookshelf (string s) to find specific books (characters in t).
    1. We use a window (like a frame) that can expand and shrink
    2. We move the right side of frame until we find all books we need
    3. Then we try to shrink it from left to make it as small as possible
    4. We keep track of the smallest valid window we've found
    """
    if not s or not t:
        return ""

    # Count how many of each character we need from t
    # Example: if t = "ABC", then t_count = {'A': 1, 'B': 1, 'C': 1}
    t_count = Counter(t)

    # Keep track of characters in our current window
    window_count = Counter()

    # How many unique characters we need to find
    required = len(t_count)
    # How many unique characters we've found with correct frequency
    current = 0

    # Window boundaries and result tracking
    left = 0
    min_window_size = float("inf")
    min_window_start = 0

    # Move the right boundary of the window
    for right, char in enumerate(s):
        # Add the new character to our window count
        window_count[char] += 1

        # If we've found enough occurrences of this character
        # Example: if we need 2 'A's and we just found the second one
        if char in t_count and window_count[char] == t_count[char]:
            current += 1

        # If we've found all characters we need, try to shrink the window
        while current == required:
            # If this window is smaller than our previous best, update it
            if right - left + 1 < min_window_size:
                min_window_size = right - left + 1
                min_window_start = left

            # Remove the leftmost character and shrink window
            left_char = s[left]
            window_count[left_char] -= 1

            # If we removed a character we needed and now don't have enough
            if left_char in t_count and window_count[left_char] < t_count[left_char]:
                current -= 1

            left += 1

    # Return the smallest window found, or empty string if none found
    return (
        ""
        if min_window_size == float("inf")
        else s[min_window_start : min_window_start + min_window_size]
    )


# Test cases
def test_min_window():
    assert min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert min_window("a", "a") == "a"
    assert min_window("a", "aa") == ""
    print("All test cases passed!")


if __name__ == "__main__":
    test_min_window()
