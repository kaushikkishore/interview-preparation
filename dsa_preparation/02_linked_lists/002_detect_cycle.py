"""
Problem: Detect Cycle
-------------------
Determine if a linked list has a cycle using Floyd's algorithm.

Time Complexity: O(n)
Space Complexity: O(1)
"""

from list_node import ListNode

def has_cycle(head: ListNode) -> bool:
    """
    Floyd's Cycle Detection Algorithm (Tortoise and Hare)
    Time: O(n), Space: O(1)
    """
    if not head or not head.next:
        return False
    
    # Initialize slow and fast pointers
    slow = head
    fast = head
    
    # Move slow by 1 and fast by 2
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        # If they meet, there's a cycle
        if slow == fast:
            return True
    
    return False

def find_cycle_start(head: ListNode) -> ListNode:
    """
    Find the node where cycle begins
    Time: O(n), Space: O(1)
    """
    if not head or not head.next:
        return None
    
    # First, detect cycle using Floyd's algorithm
    slow = fast = head
    has_cycle = False
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            has_cycle = True
            break
    
    if not has_cycle:
        return None
    
    # Move one pointer to head and keep other at meeting point
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow

# Test cases
def test_cycle_detection():
    # Create a linked list with cycle: 1->2->3->4->2
    head = ListNode(1)
    node2 = ListNode(2)
    head.next = node2
    node2.next = ListNode(3)
    node2.next.next = ListNode(4)
    node2.next.next.next = node2  # Create cycle
    
    assert has_cycle(head)
    assert find_cycle_start(head) == node2
    
    # Test list without cycle
    head2 = ListNode.create_linked_list([1, 2, 3, 4, 5])
    assert not has_cycle(head2)
    assert find_cycle_start(head2) is None
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_cycle_detection() 