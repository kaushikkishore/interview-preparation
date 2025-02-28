"""
Problem: Merge Sorted Arrays
--------------------------
Given two sorted arrays nums1 and nums2, merge nums2 into nums1 as one sorted array.
Note: nums1 has enough space at the end to hold additional elements from nums2.

Time Complexity: O(m + n) where m and n are lengths of arrays
Space Complexity: O(1) as we modify nums1 in-place

Example:
Input:
nums1 = [1,2,3,0,0,0], m = 3
nums2 = [2,5,6], n = 3
Output: [1,2,2,3,5,6]
"""


def merge_sorted_arrays(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    """
    Merge nums2 into nums1 in-place.

    Strategy:
    1. Start from the end of both arrays
    2. Compare elements and place larger one at the end of nums1
    3. Continue until all elements are placed

    Args:
        nums1: First array with extra space at end
        m: Number of actual elements in nums1
        nums2: Second array to merge
        n: Number of elements in nums2
    """
    # Initialize pointers for nums1, nums2, and merged array
    p1 = m - 1  # Last element in nums1
    p2 = n - 1  # Last element in nums2
    p = m + n - 1  # Last position in merged array

    # While there are elements to compare
    while (
        p2 >= 0
    ):  # Only need to check p2 since remaining nums1 elements are already in place
        # If nums1 has elements left and its element is larger
        if p1 >= 0 and nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1


def merge_sorted_arrays_pythonic(
    nums1: list[int], m: int, nums2: list[int], n: int
) -> None:
    """
    Alternative Pythonic solution (less efficient but more readable).
    Note: This is not the optimal solution as it uses O(m+n) space.
    """
    nums1[m:] = nums2
    nums1.sort()


# Test cases
def test_merge_sorted_arrays():
    # Test case 1: Regular case
    nums1 = [1, 2, 3, 0, 0, 0]
    merge_sorted_arrays(nums1, 3, [2, 5, 6], 3)
    assert nums1 == [1, 2, 2, 3, 5, 6]

    # Test case 2: nums1 is empty
    nums1 = [0, 0, 0]
    merge_sorted_arrays(nums1, 0, [1, 2, 3], 3)
    assert nums1 == [1, 2, 3]

    # Test case 3: nums2 is empty
    nums1 = [1, 2, 3, 0, 0, 0]
    merge_sorted_arrays(nums1, 3, [], 0)
    assert nums1 == [1, 2, 3, 0, 0, 0]

    # Test case 4: All elements in nums2 are smaller
    nums1 = [4, 5, 6, 0, 0, 0]
    merge_sorted_arrays(nums1, 3, [1, 2, 3], 3)
    assert nums1 == [1, 2, 3, 4, 5, 6]

    print("All test cases passed!")


if __name__ == "__main__":
    test_merge_sorted_arrays()
