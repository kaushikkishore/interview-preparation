class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    @staticmethod
    def create_linked_list(arr: list) -> 'ListNode':
        """Helper method to create linked list from array"""
        if not arr:
            return None
        head = ListNode(arr[0])
        current = head
        for val in arr[1:]:
            current.next = ListNode(val)
            current = current.next
        return head
    
    @staticmethod
    def to_array(head: 'ListNode') -> list:
        """Helper method to convert linked list to array"""
        result = []
        current = head
        while current:
            result.append(current.val)
            current = current.next
        return result 