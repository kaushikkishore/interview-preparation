# Hash Tables

## Problem Categories

### 1. Basic Hash Table Operations
#### Problem 1: Design HashMap
- **Problem Statement**: Implement a HashMap without using any built-in hash table libraries.
- **Example**:
  ```python
  MyHashMap hashMap = new MyHashMap();
  hashMap.put(1, 1);
  hashMap.get(1);    // returns 1
  hashMap.remove(1); // removes the mapping for 1
  ```

#### Problem 2: First Unique Character
- **Problem Statement**: Find the first non-repeating character in a string and return its index.
- **Example**:
  ```python
  Input: s = "leetcode"
  Output: 0
  Explanation: 'l' is the first non-repeating character
  ```

### 2. Advanced Applications
#### Problem 3: Group Anagrams
- **Problem Statement**: Group strings that are anagrams of each other.
- **Example**:
  ```python
  Input: ["eat","tea","tan","ate","nat","bat"]
  Output: [
    ["ate","eat","tea"],
    ["nat","tan"],
    ["bat"]
  ]
  ```

#### Problem 4: LRU Cache with HashMap
- **Problem Statement**: Design and implement a data structure for Least Recently Used (LRU) cache using HashMap and Doubly Linked List.
- **Example**:
  ```python
  LRUCache cache = new LRUCache(2); // capacity = 2
  cache.put(1, 1);
  cache.put(2, 2);
  cache.get(1);       // returns 1
  cache.put(3, 3);    // evicts key 2
  cache.get(2);       // returns -1 (not found)
  ```

