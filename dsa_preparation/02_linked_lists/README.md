# Linked Lists

## Problem Categories

### 1. Basic Operations
#### Problem 1: Reverse Linked List
- **Problem Statement**: Reverse a singly linked list iteratively and recursively.
- **Example**:
  ```python
  Input: 1->2->3->4->5
  Output: 5->4->3->2->1
  ```

#### Problem 2: Detect Cycle
- **Problem Statement**: Determine if a linked list has a cycle using Floyd's algorithm.
- **Example**:
  ```python
  Input: 1->2->3->4->2(points back to 2)
  Output: true
  ```

### 2. Advanced Operations
#### Problem 3: Merge K Sorted Lists
- **Problem Statement**: Merge k sorted linked lists into one sorted linked list.
- **Example**:
  ```python
  Input: [
    1->4->5,
    1->3->4,
    2->6
  ]
  Output: 1->1->2->3->4->4->5->6
  ```

#### Problem 4: LRU Cache
- **Problem Statement**: Implement an LRU (Least Recently Used) cache using a doubly linked list and hash map.
- **Example**:
  ```python
  cache = LRUCache(2)  # capacity = 2
  cache.put(1, 1)
  cache.put(2, 2)
  cache.get(1)       # returns 1
  cache.put(3, 3)    # evicts key 2
  ```

## Problems and Solutions

