"""

Given a linked list, reorder it so that the nodes alternate between the first half and the second half.

input
1-2-3-4-5-6

output
1-6-2-5-3-4

"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reorder(head):
    if not head or not head.next:
        return head

    slow, fast = head, head

    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    prev, curr = None, slow.next
    while curr:
        temp = curr.next
        curr.next = prev
        prev = curr
        curr = temp

    # break the link
    # This code was missing.
    slow.next = None

    first, second = head, prev

    while second:
        first_next = first.next
        second_next = second.next

        first.next = second
        second.next = first_next

        first = first_next
        second = second_next

    return head


def print_ll(head):
    while head:
        print(head.val)
        head = head.next


if __name__ == "__main__":
    head = ListNode(10)
    head.next = ListNode(20)
    head.next.next = ListNode(30)
    head.next.next.next = ListNode(40)
    head.next.next.next.next = ListNode(50)
    head.next.next.next.next.next = ListNode(60)

    new_head = reorder(head)

    while new_head:
        print(new_head.val)
        new_head = new_head.next
