"""
Problem: Implement Stack using Queues
----------------------------------
Implement a last-in-first-out (LIFO) stack using only two queues.
The implemented stack should support all the functions of a normal stack:
push, pop, top, and empty.

Time Complexity: 
- Push: O(1)
- Pop: O(n)
- Top: O(1)
- Empty: O(1)

Space Complexity: O(n)
"""

from collections import deque

class MyStack:
    """
    Example usage:
    stack = MyStack()
    stack.push(1)    # queue: [1]
    stack.push(2)    # queue: [2, 1]
    stack.top()      # returns 2
    stack.pop()      # returns 2, queue: [1]
    stack.empty()    # returns False
    """
    
    def __init__(self):
        """Initialize two queues"""
        self.q1 = deque()  # Main queue
        self.q2 = deque()  # Helper queue
        
    def push(self, x: int) -> None:
        """
        Push element x onto stack.
        New elements are added to the front by moving all elements to helper queue.
        """
        # Add new element to q2
        self.q2.append(x)
        
        # Move all elements from q1 to q2
        while self.q1:
            self.q2.append(self.q1.popleft())
            
        # Swap q1 and q2
        self.q1, self.q2 = self.q2, self.q1
        
    def pop(self) -> int:
        """Remove and return the top element."""
        if self.empty():
            return None
        return self.q1.popleft()
        
    def top(self) -> int:
        """Get the top element."""
        if self.empty():
            return None
        return self.q1[0]
        
    def empty(self) -> bool:
        """Return whether the stack is empty."""
        return len(self.q1) == 0

# Test cases
def test_stack():
    stack = MyStack()
    
    # Test push and top
    stack.push(1)
    stack.push(2)
    assert stack.top() == 2
    
    # Test pop
    assert stack.pop() == 2
    assert not stack.empty()
    assert stack.pop() == 1
    assert stack.empty()
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_stack() 