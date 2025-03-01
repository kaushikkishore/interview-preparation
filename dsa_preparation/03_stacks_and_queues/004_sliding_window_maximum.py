"""
Problem: Sliding Window Maximum
----------------------------
Given an array nums and a sliding window of size k moving from the left of the array,
find the maximum element in each window.

Time Complexity: O(n)
Space Complexity: O(k)
"""

from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """
    Find maximum in sliding window using deque.
    
    Example:
    Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
    Process:
    Window [1,3,-1]: max = 3
    Window [3,-1,-3]: max = 3
    Window [-1,-3,5]: max = 5
    Window [-3,5,3]: max = 5
    Window [5,3,6]: max = 6
    Window [3,6,7]: max = 7
    Output: [3,3,5,5,6,7]
    
    Args:
        nums: List of integers
        k: Window size
    Returns:
        List of maximum values in each window
    """
    if not nums or k == 0:
        return []
    
    result = []
    window = deque()  # Store indices
    
    # Process first k elements (first window)
    for i in range(k):
        # Remove smaller elements from back
        while window and nums[window[-1]] < nums[i]:
            window.pop()
        window.append(i)
    
    # Process rest of the elements
    for i in range(k, len(nums)):
        # First element in window is the maximum
        result.append(nums[window[0]])
        
        # Remove elements outside current window
        while window and window[0] <= i - k:
            window.popleft()
            
        # Remove smaller elements from back
        while window and nums[window[-1]] < nums[i]:
            window.pop()
            
        window.append(i)
    
    # Add maximum for last window
    result.append(nums[window[0]])
    
    return result

# Test cases
def test_sliding_window():
    # Test regular case
    nums1 = [1, 3, -1, -3, 5, 3, 6, 7]
    assert max_sliding_window(nums1, 3) == [3, 3, 5, 5, 6, 7]
    
    # Test window size = 1
    assert max_sliding_window([1, -1], 1) == [1, -1]
    
    # Test window size = array length
    assert max_sliding_window([1, 2, 3], 3) == [3]
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_sliding_window() 