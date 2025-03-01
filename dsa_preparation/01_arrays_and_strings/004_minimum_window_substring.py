"""
Problem: Minimum Window Substring
-------------------------------
Given strings s and t, find the minimum window in s that contains all characters of t.

Time Complexity Analysis:
- Optimized (Sliding Window): O(|S| + |T|)
Space Complexity Analysis:
- O(|T|) for storing character frequencies
"""


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
    need = {}
    for c in t:
        need[c] = need.get(c, 0) + 1

    # Initialize window and result variables
    left = 0
    min_start = 0
    min_length = float("inf")
    counter = len(need)  # Number of unique characters we need to find

    for right, char in enumerate(s):
        # If we find a needed character
        if char in need:
            need[char] -= 1
            if need[char] == 0:  # We've found all occurrences of this character
                counter -= 1

        # If we have all characters, try to minimize window
        while counter == 0:
            if right - left + 1 < min_length:
                min_start = left
                min_length = right - left + 1

            # Try to shrink from left
            left_char = s[left]
            if left_char in need:
                need[left_char] += 1
                if need[left_char] > 0:  # We need this character again
                    counter += 1
            left += 1

    return s[min_start : min_start + min_length] if min_length != float("inf") else ""


# Test cases
def test_min_window():
    assert min_window("ADOBECODEBANC", "ABC") == "BANC"
    # assert min_window("a", "a") == "a"
    # assert min_window("a", "aa") == ""
    print("All test cases passed!")


if __name__ == "__main__":
    test_min_window()
