"""
WOrd Search 

Given an m x n grid of characters board and a string word, return true if word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.

Leetcode - https://leetcode.com/problems/word-search/description/
"""

from typing import List
def exist(board: List[List[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])
    
    def dfs(row, col, index):
        # Base case if length matches. 
        if index == len(word):
            return True
        
        # check out of bounds 
        if (row < 0 or row >= rows or 
            col < 0 or col >= cols or 
            board[row][col] != word[index] or 
            board[row][col] == "#"):
            return False
    
        temp = board[row][col]
        board[row][col] = "#"

        # Check the left right up and down 
        found = (dfs(row-1, col, index+1 ) or
                 dfs (row +1, col, index+1) or 
                 dfs (row, col -1, index+1) or 
                 dfs(row, col+1, index+1))
        
        # backtrack 
        board[row][col] = temp

        return found 
        

    for i in range(rows):
        for j in range(cols):
            if board[i][j] == word[0]:
                if dfs(i, j, 0):
                    return True
    return False


board = [
    ['A', 'B', 'C'],
    ['D', 'E', 'F'],
    ['G', 'H', 'I']
]
word = "ABEF"
print(exist(board, word))  # Output: True

# word = "ABC"
# print(exist(board, word))  # Output: False

    

