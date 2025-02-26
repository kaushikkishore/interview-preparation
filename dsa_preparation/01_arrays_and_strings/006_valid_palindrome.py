"""
Problem: Valid Palindrome
-----------------------
Given a string, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.

Time Complexity Analysis:
- Two Pointer: O(n)
- Using Extra Space: O(n)

Space Complexity Analysis:
- Two Pointer: O(1)
- Using Extra Space: O(n)
"""


def is_palindrome_extra_space(s: str) -> bool:
    """
    Solution using extra space
    Time: O(n), Space: O(n)
    """
    # Clean the string
    cleaned = "".join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


def is_palindrome_two_pointer(s: str) -> bool:
    """
    Optimized Solution using two pointers
    Time: O(n), Space: O(1)

    Logic:
    1. Use two pointers (left and right)
    2. Skip non-alphanumeric characters
    3. Compare characters after converting to lowercase
    """
    left, right = 0, len(s) - 1

    while left < right:
        # Skip non-alphanumeric characters from left
        while left < right and not s[left].isalnum():
            left += 1

        # Skip non-alphanumeric characters from right
        while left < right and not s[right].isalnum():
            right -= 1

        # Compare characters
        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True


# Test cases
def test_valid_palindrome():
    assert is_palindrome_two_pointer("A man, a plan, a canal: Panama")
    assert not is_palindrome_two_pointer("race a car")
    assert is_palindrome_two_pointer(" ")
    assert is_palindrome_two_pointer(".,")
    print("All test cases passed!")


if __name__ == "__main__":
    test_valid_palindrome()
