"""
Problem: LRU Cache
----------------
Implement an LRU (Least Recently Used) cache using a doubly linked list and hash map.

Time Complexity: O(1) for both get and put operations
Space Complexity: O(capacity)
"""

class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        """
        Initialize LRU cache with given capacity
        """
        self.capacity = capacity
        self.cache = {}  # key -> Node
        
        # Initialize dummy head and tail
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_node(self, node: Node):
        """Add node right after head"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node: Node):
        """Remove node from linked list"""
        prev = node.prev
        new = node.next
        prev.next = new
        new.prev = prev
    
    def _move_to_head(self, node: Node):
        """Move node to front (most recently used)"""
        self._remove_node(node)
        self._add_node(node)
    
    def _pop_tail(self) -> Node:
        """Remove and return least recently used node"""
        res = self.tail.prev
        self._remove_node(res)
        return res
    
    def get(self, key: int) -> int:
        """
        Get value by key and mark as recently used
        Time: O(1)
        """
        if key in self.cache:
            node = self.cache[key]
            self._move_to_head(node)
            return node.value
        return -1
    
    def put(self, key: int, value: int) -> None:
        """
        Add or update key-value pair
        Time: O(1)
        """
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_node(new_node)
            
            if len(self.cache) > self.capacity:
                # Remove least recently used
                lru = self._pop_tail()
                del self.cache[lru.key]

# Test cases
def test_lru_cache():
    cache = LRUCache(2)
    
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)    # evicts key 2
    assert cache.get(2) == -1
    cache.put(4, 4)    # evicts key 1
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_lru_cache() 