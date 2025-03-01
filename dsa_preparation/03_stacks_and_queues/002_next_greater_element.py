"""
Problem: Next Greater Element
--------------------------
Find the next greater element for each element in an array.
For each element, find the first greater element that appears to its right.
If no greater element exists, use -1.

Time Complexity: O(n)
Space Complexity: O(n)
"""

def next_greater_element(nums: list[int]) -> list[int]:
    """
    Find next greater element using monotonic stack.
    
    Example:
    Input: [4, 5, 2, 25]
    Process:
    - For 4: Next greater is 5
    - For 5: Next greater is 25
    - For 2: Next greater is 25
    - For 25: No next greater, so -1
    Output: [5, 25, 25, -1]
    
    Args:
        nums: List of integers
    Returns:
        List of next greater elements
    """
    n = len(nums)
    result = [-1] * n  # Initialize result with -1
    stack = []  # Stack will store indices
    
    # Process all elements from right to left
    for i in range(n-1, -1, -1):
        # Remove elements smaller than current
        while stack and nums[stack[-1]] <= nums[i]:
            stack.pop()
        
        # If stack has elements, top is next greater
        if stack:
            result[i] = nums[stack[-1]]
            
        # Add current element's index to stack
        stack.append(i)
    
    return result

def next_greater_element_circular(nums: list[int]) -> list[int]:
    """
    Find next greater element in circular array.
    
    Example:
    Input: [1, 2, 1]
    Output: [2, -1, 2]
    """
    n = len(nums)
    result = [-1] * n
    stack = []
    
    # Process array twice to handle circular nature
    for i in range(2 * n - 1, -1, -1):
        while stack and nums[stack[-1] % n] <= nums[i % n]:
            stack.pop()
        
        if stack:
            result[i % n] = nums[stack[-1] % n]
            
        stack.append(i % n)
    
    return result

# Test cases
def test_next_greater():
    # Regular array
    assert next_greater_element([4, 5, 2, 25]) == [5, 25, 25, -1]
    assert next_greater_element([13, 7, 6, 12]) == [-1, 12, 12, -1]
    
    # Circular array
    assert next_greater_element_circular([1, 2, 1]) == [2, -1, 2]
    assert next_greater_element_circular([1, 2, 3, 4, 3]) == [2, 3, 4, -1, 4]
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_next_greater() 