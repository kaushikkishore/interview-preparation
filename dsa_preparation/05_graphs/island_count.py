"""
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

"""

def island_count(board):
    row, col = len(board), len(board[0])

    def dfs(r, c):
        if r < 0 or r >= row or c < 0  or c >= col or board[r][c] == '0':
            return

        board[r][c] = '0'

        # explore 
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)

    count = 0
    for r in range(row):
        for c in range(col):
            if board[r][c] == "1":
                count += 1
                dfs(r, c)

    return count


board =   [
    ["1","1","0","0","0"],
    ["1","1","0","0","0"],
    ["0","0","1","0","0"],
    ["0","0","0","1","1"]
  ]
print(island_count(board))