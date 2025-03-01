"""
Problem: Valid Parentheses
------------------------
Given a string containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

Valid string rules:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.

Time Complexity: O(n)
Space Complexity: O(n)
"""

def is_valid(s: str) -> bool:
    """
    Check if string has valid parentheses using stack.
    
    Example:
    Input: "({[]})"
    Stack changes: [ -> [( -> [({ -> [(] -> [( -> [ -> empty (valid)
    
    Args:
        s: String containing only parentheses characters
    Returns:
        bool: True if valid, False otherwise
    """
    # Map closing brackets to their corresponding opening brackets
    brackets_map = {
        ')': '(',
        '}': '{',
        ']': '['
    }
    
    stack = []
    
    for char in s:
        if char in brackets_map:  # If it's a closing bracket
            # Stack should not be empty and top should match
            if not stack or stack[-1] != brackets_map[char]:
                return False
            stack.pop()
        else:  # If it's an opening bracket
            stack.append(char)
    
    # Valid only if all brackets are matched (stack is empty)
    return len(stack) == 0

# Test cases
def test_valid_parentheses():
    assert is_valid("()")
    assert is_valid("()[]{}")
    assert is_valid("{[]}")
    assert not is_valid("(]")
    assert not is_valid("([)]")
    assert not is_valid("{")
    print("All test cases passed!")

if __name__ == "__main__":
    test_valid_parentheses() 