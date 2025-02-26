# Arrays and Strings

## Problem Categories

### 1. Two Pointer Technique
#### Problem 1: Two Sum
- **Problem Statement**: Given an array of integers `nums` and an integer `target`, return indices of the two numbers that add up to `target`.
- **Example**:
  ```python
  Input: nums = [2, 7, 11, 15], target = 9
  Output: [0, 1]
  ```

#### Problem 2: Container With Most Water
- **Problem Statement**: Given n non-negative integers representing heights of walls, find two lines that together with x-axis forms a container that holds the most water.
- **Example**:
  ```python
  Input: height = [1,8,6,2,5,4,8,3,7]
  Output: 49
  ```

### 2. Sliding Window
#### Problem 3: Longest Substring Without Repeating Characters
- **Problem Statement**: Find the length of the longest substring without repeating characters.
- **Example**:
  ```python
  Input: "abcabcbb"
  Output: 3
  Explanation: "abc" is the longest substring
  ```

#### Problem 4: Minimum Window Substring
- **Problem Statement**: Given strings s and t, find the minimum window in s that contains all characters of t.
- **Example**:
  ```python
  Input: s = "ADOBECODEBANC", t = "ABC"
  Output: "BANC"
  ```

### 3. Array Manipulation
#### Problem 5: Rotate Array
- **Problem Statement**: Given an array, rotate it to the right by k steps, where k is non-negative.
- **Example**:
  ```python
  Input: nums = [1,2,3,4,5,6,7], k = 3
  Output: [5,6,7,1,2,3,4]
  Explanation: 
  Rotate 1 step: [7,1,2,3,4,5,6]
  Rotate 2 steps: [6,7,1,2,3,4,5]
  Rotate 3 steps: [5,6,7,1,2,3,4]
  ```
- **Follow-up**: Try to solve it with O(1) extra space

### 4. String Manipulation
#### Problem 6: Valid Palindrome
- **Problem Statement**: Given a string, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.
- **Example**:
  ```python
  Input: "A man, a plan, a canal: Panama"
  Output: true
  ```

## Implementation Tips
- Always consider edge cases (empty array, single element, etc.)
- Think about time and space complexity
- Consider in-place operations when possible
