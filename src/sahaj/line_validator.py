from typing import List, Set, Union

from tambola_consts import EMPTY_CELL


class LineValidator:
    @staticmethod
    def validate_line(line: List[Union[int, str]], crossed_numbers: Set[int]) -> bool:
        """Validates if all non-empty numbers in a line are crossed"""
        return all(num in crossed_numbers for num in line if num != EMPTY_CELL)
