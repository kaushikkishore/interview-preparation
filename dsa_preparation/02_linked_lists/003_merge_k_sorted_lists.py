"""
Problem: Merge K Sorted Lists
---------------------------
Merge k sorted linked lists into one sorted linked list.

Time Complexity: O(N log k) where N is total nodes and k is number of lists
Space Complexity: O(1) excluding output list
"""

from list_node import ListNode
import heapq


def merge_k_lists(lists: list[ListNode]) -> ListNode:
    """
    Merges k sorted linked lists into a single sorted linked list using a min heap.

    The basic idea is:
    1. Use a min heap to always track the smallest value among all list heads
    2. Keep pulling the smallest value and adding its next node to the heap

    Args:
        lists: Array of heads of k sorted linked lists
    Returns:
        Head of the merged sorted linked list
    """

    # We need this wrapper class because ListNode doesn't implement comparison methods
    # Python's heapq needs to compare elements, so we provide a custom comparison
    class ListNodeWrapper:
        def __init__(self, node):
            self.node = node

        def __lt__(self, other):
            # Define how to compare two nodes (by their values)
            return self.node.val < other.node.val

    # Initialize the min heap with the first node from each list
    # This means we'll start with k nodes in our heap
    heap = []
    for i, lst in enumerate(lists):
        if lst:  # Only add non-empty lists
            heapq.heappush(heap, ListNodeWrapper(lst))

    # Dummy node helps avoid special cases for the head of our result list
    # current will be used to build our result list
    dummy = ListNode(0)
    current = dummy

    # Keep going until we've processed all nodes
    while heap:
        # Pop the smallest value from the heap
        wrapper = heapq.heappop(heap)
        node = wrapper.node

        # Add this smallest value to our result list
        current.next = ListNode(node.val)
        current = current.next

        # If this node has a next value, add it to the heap
        # This maintains our k-way merge by always keeping track
        # of the next potential value from each list
        if node.next:
            heapq.heappush(heap, ListNodeWrapper(node.next))

    return dummy.next  # Return everything after our dummy node


# Test cases
def test_merge_k_lists():
    # Create test lists
    list1 = ListNode.create_linked_list([1, 4, 5])
    list2 = ListNode.create_linked_list([1, 3, 4])
    list3 = ListNode.create_linked_list([2, 6])

    result = merge_k_lists([list1, list2, list3])
    assert ListNode.to_array(result) == [1, 1, 2, 3, 4, 4, 5, 6]

    # Test empty lists
    assert merge_k_lists([]) is None

    print("All test cases passed!")


if __name__ == "__main__":
    test_merge_k_lists()
