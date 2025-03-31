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
from collections import deque
def island_count(board):
    rows, cols = len(board), len(board[0])

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0  or c >= cols or board[r][c] == '0':
            return

        board[r][c] = '0'

        # explore 
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)

    def bfs(r, c):
        queue = deque()
        queue.append((r,c))
        board[r][c] = '0'

        while queue:
            row, col = queue.popleft()
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr = row + dr 
                nc = col + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == "1":
                    board[nr][nc] = "0"
                    queue.append((nr,nc))

    count = 0
    for r in range(rows):
        for c in range(cols):
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