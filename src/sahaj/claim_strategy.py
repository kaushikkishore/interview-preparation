from typing import List, Set, Union

from line_validator import LineValidator
from tambola_consts import EMPTY_CELL, EARLY_FIVE_COUNT


class ClaimStrategy:
    @staticmethod
    def validate_top_line(
        ticket: List[List[Union[int, str]]], crossed_numbers: Set[int]
    ) -> bool:
        return LineValidator.validate_line(ticket[0], crossed_numbers)

    @staticmethod
    def validate_middle_line(
        ticket: List[List[Union[int, str]]], crossed_numbers: Set[int]
    ) -> bool:
        return LineValidator.validate_line(ticket[1], crossed_numbers)

    @staticmethod
    def validate_bottom_line(
        ticket: List[List[Union[int, str]]], crossed_numbers: Set[int]
    ) -> bool:
        return LineValidator.validate_line(ticket[2], crossed_numbers)

    # @staticmethod
    # def validate_row(index: int) -> bool:
    #     return

    @staticmethod
    def validate_full_house(
        ticket: List[List[Union[int, str]]], crossed_numbers: Set[int]
    ) -> bool:
        return all(LineValidator.validate_line(row, crossed_numbers) for row in ticket)

    @staticmethod
    def validate_early_five(
        ticket: List[List[Union[int, str]]], crossed_numbers: Set[int]
    ) -> bool:
        crossed_count = sum(
            1
            for row in ticket
            for num in row
            if num != EMPTY_CELL and num in crossed_numbers
        )
        return crossed_count >= EARLY_FIVE_COUNT

    @staticmethod
    def validate_any_diagonal(
        ticket: List[List[Union[int, str]]], crossed_numbers: Set[int]
    ) -> bool:
        """
        Validate any of the diagonals are crossed then its true
        Find out all diagonals
        """

        """
        if row or column is going out of bound then skip. 
        """

        def dfs(row, col, found_ones):
            if row < 0 or col < 0 or row >= len(ticket) or col >= len(ticket[0]):
                return None

            if ticket[row][col] != EMPTY_CELL:
                found_ones.add(ticket[row][col])

            dfs(row + 1, col + 1, found_ones)
            # dfs(row - 1, col - 1, found_ones)
            # dfs(row - 2, col - 2, found_ones)

        # Iterate over all the rows
        for i in range(len(ticket[0])):
            # define a new set so that we can store the diagonal ones
            all_found_ones = set()
            # Recurse for the dfs
            dfs(0, i, all_found_ones)
            # validate the all found one in the crossed numbers.
            if len(all_found_ones) == 3:
                if all(item in crossed_numbers for item in all_found_ones):
                    return True

        return False


if __name__ == "__main__":
    ticket = [
        [4, 16, "_", "_", 48, "_", 63, 76, "_"],
        [7, "_", 23, 38, "_", 52, "_", "_", 80],
        [9, "_", 25, "_", "_", 56, 64, "_", 83],
    ]
    numbers_announced = [90, 4, 48, 52, 64, 16, 76, 48]
    validator = ClaimStrategy()
    print(validator.validate_any_diagonal(ticket, set(numbers_announced)))
