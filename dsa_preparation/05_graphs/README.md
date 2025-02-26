# Graphs

## Problem Categories

### 1. Graph Traversal
#### Problem 1: Number of Islands
- **Problem Statement**: Given a 2D grid of '1's (land) and '0's (water), count the number of islands.
- **Example**:
  ```python
  Input: 
  [
    ["1","1","0","0","0"],
    ["1","1","0","0","0"],
    ["0","0","1","0","0"],
    ["0","0","0","1","1"]
  ]
  Output: 3
  ```

#### Problem 2: Course Schedule
- **Problem Statement**: Given prerequisites for courses, determine if it's possible to finish all courses (detect cycle in directed graph).
- **Example**:
  ```python
  Input: numCourses = 2, prerequisites = [[1,0]]
  Output: true
  Explanation: Can take course 0 then 1
  ```

### 2. Shortest Path
#### Problem 3: Network Delay Time
- **Problem Statement**: Given a network of nodes and times for signals to travel, find how long it takes for all nodes to receive the signal.
- **Example**:
  ```python
  Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
  Output: 2
  ```

#### Problem 4: Word Ladder
- **Problem Statement**: Transform one word to another by changing one character at a time, using a dictionary of valid words.
- **Example**:
  ```python
  Input: 
  beginWord = "hit"
  endWord = "cog"
  wordList = ["hot","dot","dog","lot","log","cog"]
  Output: 5
  Explanation: hit -> hot -> dot -> dog -> cog
  ```

## Problems and Solutions

