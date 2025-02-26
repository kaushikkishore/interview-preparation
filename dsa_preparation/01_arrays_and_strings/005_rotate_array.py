"""
Problem: Rotate Array
-------------------
Given an array, rotate it to the right by k steps, where k is non-negative.

Time Complexity Analysis:
- Using Extra Array: O(n)
- Using Reversal: O(n)
- Using Cyclic Replacements: O(n)

Space Complexity Analysis:
- Using Extra Array: O(n)
- Using Reversal: O(1)
- Using Cyclic Replacements: O(1)
"""

def rotate_extra_space(nums: list[int], k: int) -> None:
    """
    Solution using extra space
    Time: O(n), Space: O(n)
    """
    n = len(nums)
    k = k % n  # Handle k > n case
    temp = nums.copy()
    
    for i in range(n):
        nums[(i + k) % n] = temp[i]

def rotate_reversal(nums: list[int], k: int) -> None:
    """
    Optimized Solution using array reversal
    Time: O(n), Space: O(1)
    
    Logic:
    1. Reverse entire array
    2. Reverse first k elements
    3. Reverse remaining elements
    """
    def reverse(arr: list[int], start: int, end: int) -> None:
        while start < end:
            arr[start], arr[end] = arr[end], arr[start]
            start += 1
            end -= 1
    
    n = len(nums)
    k = k % n  # Handle k > n case
    
    reverse(nums, 0, n-1)    # Reverse entire array
    reverse(nums, 0, k-1)    # Reverse first k elements
    reverse(nums, k, n-1)    # Reverse remaining elements

def rotate_cyclic(nums: list[int], k: int) -> None:
    """
    Optimized Solution using cyclic replacements
    Time: O(n), Space: O(1)
    
    Logic:
    1. Move each element to its final position
    2. Keep track of starting position and elements moved
    """
    n = len(nums)
    k = k % n
    count = 0
    
    start = 0
    while count < n:
        current = start
        prev = nums[start]
        
        while True:
            next_idx = (current + k) % n
            nums[next_idx], prev = prev, nums[next_idx]
            current = next_idx
            count += 1
            
            if start == current:
                break
        
        start += 1

# Test cases
def test_rotate():
    # Test reversal method
    nums1 = [1,2,3,4,5,6,7]
    rotate_reversal(nums1, 3)
    assert nums1 == [5,6,7,1,2,3,4]
    
    # Test cyclic method
    nums2 = [1,2,3,4,5,6,7]
    rotate_cyclic(nums2, 3)
    assert nums2 == [5,6,7,1,2,3,4]
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_rotate() 