"""
Given a string and an integer k, find the number of substrings in which all the different characters occur exactly k times.

"""

"""
ooneTwoTThreeFour
k = 2
["ee","oo","TT"]

count  - Number of subtrings 


dict - counting chars 

"""


def get_subtring_count(s: str, k: int):
    """ """
    # if no string is found
    print("input", s, k)
    if not s:
        return 0

    # in case string is small and k is large
    if k > len(s):
        return 0

    print("going to evaluate")

    left = 0
    right = k
    total_count = 0

    while left <= len(s):
        # TODO if right is more than the length of the sring overflowing

        if len(s) - left < k:
            print("continue", left)
            break

        extracted = s[left:right]

        print("extracted", extracted)

        uq_keys = {}

        for e in extracted:
            if e in uq_keys:
                uq_keys[e] += 1
            else:
                uq_keys[e] = 1

        print("uq_keys", uq_keys)

        print("values", uq_keys.values())
        for key in uq_keys.keys():
            if uq_keys[key] == k:
                total_count += 1
                break

        left += 1
        right += 1

    return total_count


# print(get_subtring_count("ooneTwoTThreeFour", 2))


print(get_subtring_count("aabbcc", 2))  # aa, bb, cc, aabb, bbcc, aabbcc # 6

# print(get_subtring_count("ababcbcbcb", 2))

"""
aabbcc
a abbcc
aa bbcc



aab bcc
aabb cc
aabbc c
aabbcc 

a
aa 
aab
aabb
aabbc 
aabbcc

aa 
aab 



                     aabbcc
                a                abbcc




"""


"""
SOLUTION FROM GPT 
"""

from collections import Counter


def count_substrings_with_k_freq(s, k):
    """
    Find the number of substrings in which all different characters occur exactly k times.

    Args:
        s (str): The input string
        k (int): The required frequency of each character

    Returns:
        int: The number of valid substrings
    """
    if not s or k <= 0:
        return 0

    result = 0
    n = len(s)

    # Try all possible substrings
    for start in range(n):
        # Use Counter to track character frequencies
        char_count = Counter()

        for end in range(start, n):
            # Add the current character
            char_count[s[end]] += 1

            # Check if all characters have exactly k occurrences
            valid = True
            for count in char_count.values():
                if count != k:
                    valid = False
                    break

            if valid:
                result += 1

    return result


# Optimized version with early stopping
def count_substrings_with_k_freq_optimized(s, k):
    """
    Find the number of substrings in which all different characters occur exactly k times.
    Optimized version that stops checking when a character exceeds k occurrences.

    Args:
        s (str): The input string
        k (int): The required frequency of each character

    Returns:
        int: The number of valid substrings
    """
    if not s or k <= 0:
        return 0

    result = 0
    n = len(s)

    for start in range(n):
        char_count = Counter()

        for end in range(start, n):
            # Add current character
            char_count[s[end]] += 1

            # If any character exceeds k, this and longer substrings won't be valid
            if char_count[s[end]] > k:
                break

            # Check if all characters have exactly k occurrences
            if all(count == k for count in char_count.values()):
                result += 1

    return result


# Example usage
s = "aabbcc"
k = 2
print(
    count_substrings_with_k_freq_optimized(s, k)
)  # Expected: 6 (substrings "aa", "bb", "cc", "aabb", "bbcc", "aabbcc")

# More examples
print(
    count_substrings_with_k_freq_optimized("aaabbb", 3)
)  # Expected: 2 (substrings "aaa", "bbb")
print(
    count_substrings_with_k_freq_optimized("abc", 1)
)  # Expected: 3 (substrings "a", "b", "c")
print(
    count_substrings_with_k_freq_optimized("ababcc", 2)
)  # Expected: 2 (substrings "abab", "cc")
