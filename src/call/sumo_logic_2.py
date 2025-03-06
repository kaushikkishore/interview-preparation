# https://www.geeksforgeeks.org/number-substrings-count-character-k/
# https://leetcode.com/problems/count-complete-substrings/



def substrings(s, k):
    MAX_CHAR = 26
    res = 0  # Initialize result

    # Pick a starting point
    for i in range(len(s)):
        # Initialize all frequencies as 0 for this starting point
        freq = [0] * MAX_CHAR

        # Consider all substrings starting from i
        for j in range(i, len(s)):
            # Increment frequency of current character
            index = ord(s[j]) - ord("a")
            freq[index] += 1

            # If frequency becomes more than k, we can't have more substrings
            # starting with i
            if freq[index] > k:
                break

            # If frequency becomes k, then check other frequencies as well
            elif freq[index] == k and all(f == 0 or f == k for f in freq):
                res += 1

    return res


# Example usage
s1 = "aabbcc"
k1 = 2
print(substrings(s1, k1))  # Output: 6

# s2 = "aabbc"
# k2 = 2
# print(substrings(s2, k2))  # Output: 3
