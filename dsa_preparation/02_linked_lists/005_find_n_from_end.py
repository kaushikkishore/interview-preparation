"""

Remove the last nth item from linked list 

"""


class Node: 
    def __init__(self, value = 0, next = None):
        self.value = value
        self.next = next 
    

"""
2 pass solution 
"""
def remove_from_last(head, index):
    count = 0

    current = head 

    while current:
        count += 1
        current = current.next
    
    print(f"total count of list {count}")

    if index > count:
        return None 

    # index to remove 
    idx_to_remove = count - index

    current = head 

    for i in range(idx_to_remove -1):
        current = current.next
    
    current.next = current.next.next 
    return head 



def print_linked_list(result):
    while result:
        print(result.value)
        result = result.next



"""
ONE PASS SOLUTION 
"""

def one_pass_remove(head, index):
    dummy = Node(0)
    dummy.next = head 

    first = dummy 
    sec = dummy 

    for i in range(index+1):
        if not sec:
            return head
        sec = sec.next 
    
    while sec: 
        sec = sec.next
        first = first.next

    first.next = first.next.next

    return dummy.next 
    

    
    

# 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7
seven = Node(7)
six = Node(6, seven)
five = Node(5, six)
four = Node(4, five)
three = Node(3, four)
sec = Node(2, three)

first = Node(1, sec)

print_linked_list(one_pass_remove(first, 4))

    