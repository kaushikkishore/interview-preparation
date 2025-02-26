"""
Problem: Reverse Linked List
--------------------------
Reverse a singly linked list iteratively and recursively.

Time Complexity: O(n)
Space Complexity: 
- Iterative: O(1)
- Recursive: O(n) due to call stack
"""

from list_node import ListNode

def reverse_iterative(head: ListNode) -> ListNode:
    """
    Iterative approach using three pointers
    Time: O(n), Space: O(1)
    """
    prev = None
    current = head
    
    while current:
        next_temp = current.next  # Store next
        current.next = prev       # Reverse link
        prev = current           # Move prev forward
        current = next_temp      # Move current forward
    
    return prev

def reverse_recursive(head: ListNode) -> ListNode:
    """
    Recursive approach
    Time: O(n), Space: O(n)
    """
    # Base cases
    if not head or not head.next:
        return head
    
    # Recursive case
    rest = reverse_recursive(head.next)
    head.next.next = head  # Reverse link
    head.next = None       # Set original next to None
    
    return rest

# Test cases
def test_reverse_linked_list():
    # Test iterative
    head1 = ListNode.create_linked_list([1, 2, 3, 4, 5])
    reversed1 = reverse_iterative(head1)
    assert ListNode.to_array(reversed1) == [5, 4, 3, 2, 1]
    
    # Test recursive
    head2 = ListNode.create_linked_list([1, 2, 3, 4, 5])
    reversed2 = reverse_recursive(head2)
    assert ListNode.to_array(reversed2) == [5, 4, 3, 2, 1]
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_reverse_linked_list() 