"""
Depth-First Search (DFS) Algorithm Explanation
-------------------------------------------
DFS is a graph traversal algorithm that explores as far as possible along each branch before backtracking.

Key Concepts:
1. Stack-based (recursive or iterative)
2. Visits vertices in depth-first order
3. Uses backtracking to explore all paths
4. Can be used for:
   - Path finding
   - Cycle detection
   - Topological sorting
   - Maze solving
   - Connected components

Time Complexity: O(V + E) where V = vertices, E = edges
Space Complexity: O(V) for recursion stack
"""

from typing import List, Set, Dict


class Graph:
    def __init__(self):
        """Initialize an empty graph using adjacency list"""
        self.graph: Dict[int, List[int]] = {}
        self.visited: Set[int] = set()

    def add_edge(self, u: int, v: int) -> None:
        """Add an edge to the graph"""
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)
        self.graph[v].append(u)  # For undirected graph

    def dfs_recursive(self, start: int) -> None:
        """
        Recursive DFS implementation

        Steps:
        1. Mark current vertex as visited
        2. Process current vertex (print, store, etc.)
        3. For each unvisited neighbor:
           - Recursively call DFS
        """
        # Mark current vertex as visited
        self.visited.add(start)
        print(f"Visiting vertex: {start}")

        # Visit all neighbors
        for neighbor in self.graph[start]:
            if neighbor not in self.visited:
                self.dfs_recursive(neighbor)

    def dfs_iterative(self, start: int) -> None:
        """
        Iterative DFS implementation using stack

        Steps:
        1. Push start vertex to stack
        2. While stack is not empty:
           - Pop vertex from stack
           - If not visited:
             * Mark as visited
             * Process vertex
             * Push all unvisited neighbors
        """
        stack = [start]
        self.visited.clear()  # Clear previous visited set

        while stack:
            vertex = stack.pop()
            if vertex not in self.visited:
                self.visited.add(vertex)
                print(f"Visiting vertex: {vertex}")

                # Add unvisited neighbors to stack
                for neighbor in reversed(self.graph[vertex]):
                    if neighbor not in self.visited:
                        stack.append(neighbor)

    def has_path(self, start: int, end: int) -> bool:
        """
        Check if path exists between start and end using DFS

        Steps:
        1. Mark current vertex as visited
        2. If current vertex is end, return True
        3. For each unvisited neighbor:
           - Recursively check for path
        4. If no path found, return False
        """
        if start == end:
            return True

        self.visited.add(start)

        for neighbor in self.graph[start]:
            if neighbor not in self.visited:
                if self.has_path(neighbor, end):
                    return True
        return False


# Example usage and visualization
def demonstrate_dfs():
    # Create a sample graph:
    # 0 --- 1
    # |     |
    # 2 --- 3

    g = Graph()
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 3)

    print("Recursive DFS starting from vertex 0:")
    g.visited.clear()
    g.dfs_recursive(0)

    print("\nIterative DFS starting from vertex 0:")
    g.dfs_iterative(0)

    print("\nChecking path from 0 to 3:")
    g.visited.clear()
    print(f"Path exists: {g.has_path(0, 3)}")


# Common DFS Applications
def dfs_applications():
    """
    1. Cycle Detection
    -----------------
    - Keep track of vertices in current recursion stack
    - If we visit a vertex that's in current stack, cycle exists

    2. Topological Sorting
    ---------------------
    - Only works on Directed Acyclic Graphs (DAG)
    - Add vertex to result after visiting all neighbors

    3. Connected Components
    ----------------------
    - Run DFS from each unvisited vertex
    - Each DFS call finds one connected component

    4. Maze Solving
    --------------
    - Grid represents maze
    - DFS finds path from start to end
    - Backtrack when dead end is reached
    """
    pass


if __name__ == "__main__":
    demonstrate_dfs()
