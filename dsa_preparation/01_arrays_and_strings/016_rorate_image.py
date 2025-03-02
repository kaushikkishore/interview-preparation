# https://leetcode.com/problems/rotate-image/description/?envType=problem-list-v2&envId=array

# You are given an n x n 2D matrix representing an image, rotate the image by 90 degrees (clockwise).

# You have to rotate the image in-place, which means you have to modify the input 2D matrix directly. DO NOT allocate another 2D matrix and do the rotation.


# Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
# Output: [[7,4,1],[8,5,2],[9,6,3]]

""" """

from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)

        # Step 1: Transpose the matrix
        for i in range(n):
            for j in range(i, n):
                # Swap elements across diagonal
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        # Step 2: Reverse each row
        for i in range(n):
            matrix[i].reverse()


Solution().rotate([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


def test_rotate():
    # Test case 1: 3x3 matrix
    matrix1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    Solution().rotate(matrix1)
    assert matrix1 == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

    # Test case 2: 4x4 matrix
    matrix2 = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
    Solution().rotate(matrix2)
    assert matrix2 == [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]

    # Test case 3: 2x2 matrix
    matrix3 = [[1, 2], [3, 4]]
    Solution().rotate(matrix3)
    assert matrix3 == [[3, 1], [4, 2]]

    # Test case 4: 1x1 matrix
    matrix4 = [[1]]
    Solution().rotate(matrix4)
    assert matrix4 == [[1]]

    print("All test cases passed!")


if __name__ == "__main__":
    test_rotate()
