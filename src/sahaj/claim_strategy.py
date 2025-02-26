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
