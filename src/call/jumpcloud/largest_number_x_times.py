# Problem Description:
# ------------------
# Given an array A of integers, find the largest integer X such that X appears
# exactly X times in the array.
#
# For example:
# - If A = [3, 8, 2, 3, 3, 2], then 3 appears exactly 3 times, so the answer is 3.
# - If A = [7, 1, 2, 8, 2], then 2 appears exactly 2 times, so the answer is 2.
# - If A = [5, 5, 5, 1, 5], no value appears exactly its own number of times, so return 0.
#
# Only consider values that are between 1 and n (inclusive), where n is the length
# of the array, since values greater than n cannot appear n times in an array of length n.
#
# Return 0 if no such value exists.


def solution(A):
    # Get the length of the array
    n = len(A)

    # We only need to count values that are at most n
    # since a value greater than n cannot occur n times in an array of length n
    count = {}

    for num in A:
        # Only consider values in the range [1, n]
        if 1 <= num <= n:
            if num in count:
                count[num] += 1
            else:
                count[num] = 1

    max_value = 0

    # Find the largest value that occurs exactly its value times
    for value, occurrences in count.items():
        if value == occurrences and value > max_value:
            max_value = value

    return max_value


# Test cases
if __name__ == "__main__":
    # Test case 1: Normal case with a valid answer
    test1 = [3, 8, 2, 3, 3, 2]  # 3 appears 3 times
    print(f"Test 1: {test1} => {solution(test1)}")  # Expected output: 3

    # Test case 2: Another normal case with a valid answer
    test2 = [7, 1, 2, 8, 2]  # 2 appears 2 times
    print(f"Test 2: {test2} => {solution(test2)}")  # Expected output: 2

    # Test case 3: No value appears exactly its value times
    test3 = [5, 5, 5, 1, 5]  # 5 appears 4 times, 1 appears 1 time but we want the max
    print(f"Test 3: {test3} => {solution(test3)}")  # Expected output: 1

    # Test case 4: Multiple values appear exactly their value times
    test4 = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]  # 1 appears 1 time, 2 appears 2 times, etc.
    print(f"Test 4: {test4} => {solution(test4)}")  # Expected output: 4

    # Test case 5: Empty array
    test5 = []
    print(f"Test 5: {test5} => {solution(test5)}")  # Expected output: 0

    # Test case 6: Array with values outside the valid range
    test6 = [10, 20, 30, 1]  # Only 1 is in range 1-4, and 1 appears 1 time
    print(f"Test 6: {test6} => {solution(test6)}")  # Expected output: 1

    # Test case 7: Array with negative numbers
    test7 = [-3, -2, -1, 1, 1]  # Negative numbers are ignored
    print(f"Test 7: {test7} => {solution(test7)}")  # Expected output: 1

    # Test case 8: Array with all zeros
    test8 = [0, 0, 0, 0]  # 0 is out of range (1-4)
    print(f"Test 8: {test8} => {solution(test8)}")  # Expected output: 0
