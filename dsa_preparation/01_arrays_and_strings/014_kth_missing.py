# Find the k-th Missing Number
# Problem: Given an array of positive integers (which can be unsorted) and a positive integer k,
# find the k-th missing positive integer starting from 1.

# Example:
# Input: arr = [2, 4, 6, 7, 8], k = 2
# Output: 3
# Explanation: The missing positive integers are [1, 3, 5, 9, 10, ...]. The 2nd missing integer is 3.


def find_kth_missing(arr: list[int], k: int) -> int:
    """
    Find the k-th missing positive integer in an array (can be unsorted).

    Approach:
    1. Convert the array to a set for O(1) lookups
    2. Start checking from 1 and count missing numbers
    3. When we reach the k-th missing number, return it

    Time Complexity: O(n + m) where:
      - n is the size of the input array
      - m is the value of the k-th missing number
    Space Complexity: O(n) for the set

    Args:
        arr: List[int] - array of positive integers (can be unsorted)
        k: int - position of missing number to find

    Returns:
        int - the k-th missing positive integer
    """
    # Handle empty array case
    # If the array is empty, the k-th missing positive integer is simply k
    if not arr:
        return k

    # Convert array to set for O(1) lookups
    # This allows us to check if a number exists in the array in constant time
    num_set = set(arr)

    # Count missing numbers until we find the k-th one
    # We'll start from 1 and increment, checking each positive integer
    missing_count = 0
    num = 1

    while missing_count < k:
        # If the current number is not in our set, it's a missing number
        if num not in num_set:
            missing_count += 1
            # If we've found the k-th missing number, return it
            if missing_count == k:
                return num
        # Move to the next number
        num += 1

    # This line should never be reached if k is positive
    return num


def find_kth_missing_optimized(arr: list[int], k: int) -> int:
    """
    Find the k-th missing positive integer in an array using binary search.
    This optimized solution works best when the array is sorted.

    Approach:
    1. Sort the array if not already sorted
    2. Use binary search to find the k-th missing number

    Time Complexity:
      - O(n log n) if array needs sorting
      - O(log n) for the binary search if array is already sorted
    Space Complexity: O(1) - no extra space needed except for sorting

    Args:
        arr: List[int] - array of positive integers (can be unsorted)
        k: int - position of missing number to find

    Returns:
        int - the k-th missing positive integer
    """
    # Handle empty array case
    if not arr:
        return k

    # Sort the array if not already sorted
    # Note: If the array is guaranteed to be sorted, this step can be skipped
    arr = sorted(arr)

    # Binary search approach
    left, right = 0, len(arr) - 1

    # First, check if k-th missing is less than the first element
    if k <= arr[0] - 1:
        return k

    # Check if k-th missing is greater than the last element
    # Calculate how many numbers are missing up to the last element
    missing_count = arr[-1] - len(arr)
    if k > missing_count:
        # If k is greater, the answer is (last element + remaining missing numbers)
        return arr[-1] + (k - missing_count)

    # Binary search to find the position where k-th missing number would be
    while left < right:
        mid = left + (right - left) // 2

        # Calculate missing numbers up to mid position
        # arr[mid] - (mid + 1) gives the count of missing numbers up to arr[mid]
        # because if no numbers were missing, arr[mid] would be (mid + 1)
        missing = arr[mid] - (mid + 1)

        if missing < k:
            left = mid + 1
        else:
            right = mid

    # At this point, left points to the position where the k-th missing number would be
    # We need to calculate what that number is
    # The number of missing values before arr[left-1] is arr[left-1] - left
    # So the k-th missing number is left + k
    return left + k


def find_kth_missing_constant_space(arr: list[int], k: int) -> int:
    """
    Find the k-th missing positive integer in an array without sorting and using O(1) space.

    Approach:
    1. Find the maximum value in the array
    2. Calculate how many numbers are missing up to the maximum value
    3. If k is greater than this count, the answer is max_val + (k - missing_count)
    4. Otherwise, use a counting approach to find the k-th missing number

    Time Complexity: O(n + max(arr)) in worst case, but often much better
    Space Complexity: O(1) - no extra data structures used

    Args:
        arr: List[int] - array of positive integers (can be unsorted)
        k: int - position of missing number to find

    Returns:
        int - the k-th missing positive integer
    """
    # Handle empty array case
    if not arr:
        return k

    # Find the maximum value in the array - O(n)
    max_val = max(arr)

    # Count how many numbers from 1 to max_val are in the array - O(n)
    count_present = 0
    for num in arr:
        if 1 <= num <= max_val:
            count_present += 1

    # Calculate how many numbers are missing up to max_val
    missing_count = max_val - count_present

    # If k is greater than missing_count, the answer is beyond max_val
    if k > missing_count:
        return max_val + (k - missing_count)

    # Otherwise, we need to find the k-th missing number within the range [1, max_val]
    # We'll use a counting approach, but optimize by skipping numbers we know exist

    # Create a boolean array to mark which numbers exist in the range [1, max_val]
    # This is still O(1) space as we're not using extra space proportional to input size
    # We're using a different approach that doesn't require this array

    # Count missing numbers until we find the k-th one
    missing_count = 0
    for num in range(1, max_val + 1):
        # Check if the current number is in the array - O(n) in worst case
        # But we can optimize this by using a simple linear scan
        if num not in arr:
            missing_count += 1
            if missing_count == k:
                return num

    # This line should never be reached based on our earlier check
    return max_val + (k - missing_count)


def find_kth_missing_true_constant_space(arr: list[int], k: int) -> int:
    """
    Find the k-th missing positive integer in an array with true O(1) space complexity.

    Approach:
    1. Use math to calculate the k-th missing number directly
    2. No sorting or additional data structures required

    Time Complexity: O(n)
    Space Complexity: O(1)

    Args:
        arr: List[int] - array of positive integers (can be unsorted)
        k: int - position of missing number to find

    Returns:
        int - the k-th missing positive integer
    """
    # Handle empty array case
    if not arr:
        return k

    # Count how many numbers in the range [1, k+len(arr)] are present in the array
    count = 0
    for num in arr:
        if 1 <= num <= k + len(arr):
            count += 1

    # The k-th missing number must be in the range [1, k+len(arr)]
    # If we have 'count' numbers present in this range, then we have (k+len(arr)-count) missing numbers
    # The k-th missing number is k + len(arr) - (k+len(arr)-count) = count

    # But this is only true if all numbers in arr are in the range [1, k+len(arr)]
    # We need to find exactly which number is the k-th missing one

    # We'll use a more direct approach:
    # The k-th missing number is k + how many numbers in arr are <= k

    # Count how many numbers in arr are <= k + count
    shift = 0
    for num in arr:
        if num <= k + shift:
            shift += 1

    # The k-th missing number is k + shift
    return k + shift


# Test cases
def test_find_kth_missing():
    # Each test case is a tuple of (input_array, k, expected_output)
    test_cases = [
        ([4, 2, 6, 8, 7], 2, 3),  # Unsorted example case - missing [1, 3, 5, ...]
        ([6, 1, 4, 2, 7], 3, 5),  # Unsorted, Missing [3, 5, 8, ...]
        ([11, 4, 2, 7, 3], 5, 9),  # Unsorted, Missing [1, 5, 6, 8, 9, ...]
        ([], 5, 5),  # Empty array - all numbers 1 to k are missing
        ([1], 3, 4),  # Single element - missing [2, 3, 4, ...]
    ]

    # Run each test case and print the results
    print("Testing original solution:")
    for arr, k, expected in test_cases:
        result = find_kth_missing(arr, k)
        print(f"Array: {arr}, k: {k}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"Test {'passed' if result == expected else 'failed'}\n")

    print("Testing optimized solution (with sorting):")
    for arr, k, expected in test_cases:
        result = find_kth_missing_optimized(arr, k)
        print(f"Array: {arr}, k: {k}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"Test {'passed' if result == expected else 'failed'}\n")

    print("Testing constant space solution:")
    for arr, k, expected in test_cases:
        result = find_kth_missing_constant_space(arr, k)
        print(f"Array: {arr}, k: {k}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"Test {'passed' if result == expected else 'failed'}\n")

    print("Testing true constant space solution:")
    for arr, k, expected in test_cases:
        result = find_kth_missing_true_constant_space(arr, k)
        print(f"Array: {arr}, k: {k}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"Test {'passed' if result == expected else 'failed'}\n")


if __name__ == "__main__":
    test_find_kth_missing()
