# Find the k-th Missing Number


# Example:
# Input: arr = [2, 4, 6, 7, 8], k = 2
# Output: 3


def find_kth_missing(arr, k):
    """
    Find the k-th missing positive integer in an array (can be unsorted).

    Args:
        arr: List[int] - array of positive integers (can be unsorted)
        k: int - position of missing number to find

    Returns:
        int - the k-th missing positive integer
    """
    # Handle empty array case
    if not arr:
        return k

    # Convert array to set for O(1) lookups
    num_set = set(arr)

    # Count missing numbers until we find the k-th one
    missing_count = 0
    num = 1

    while missing_count < k:
        if num not in num_set:
            missing_count += 1
            if missing_count == k:
                return num
        num += 1

    return num


# Test cases
def test_find_kth_missing():
    test_cases = [
        ([4, 2, 6, 8, 7], 2, 3),  # Unsorted example case
        ([6, 1, 4, 2, 7], 3, 5),  # Unsorted, Missing 3, 5, 8...
        ([11, 4, 2, 7, 3], 5, 9),  # Unsorted, Missing 1, 5, 6, 8, 9...
        ([], 5, 5),  # Empty array
        ([1], 3, 4),  # Single element
    ]

    for arr, k, expected in test_cases:
        result = find_kth_missing(arr, k)
        print(f"Array: {arr}, k: {k}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"Test {'passed' if result == expected else 'failed'}\n")


if __name__ == "__main__":
    test_find_kth_missing()
