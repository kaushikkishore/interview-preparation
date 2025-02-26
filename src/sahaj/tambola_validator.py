from typing import List, Set, Dict, Callable, Union

from claim_strategy import ClaimStrategy
from tambola_consts import (
    TOP_LINE,
    MIDDLE_LINE,
    BOTTOM_LINE,
    FULL_HOUSE,
    EARLY_FIVE,
    ACCEPTED,
    REJECTED,
    TICKET_ROW_SIZE,
    TICKET_COLUMN_SIZE,
)


class TambolaValidator:
    def __init__(self) -> None:
        self._claim_validators: Dict[
            str, Callable[[List[List[Union[int, str]]], Set[int]], bool]
        ] = {
            TOP_LINE: ClaimStrategy.validate_top_line,
            MIDDLE_LINE: ClaimStrategy.validate_middle_line,
            BOTTOM_LINE: ClaimStrategy.validate_bottom_line,
            FULL_HOUSE: ClaimStrategy.validate_full_house,
            EARLY_FIVE: ClaimStrategy.validate_early_five,
        }

        self._line_checkers: Dict[
            str, Callable[[List[List[Union[int, str]]], int], bool]
        ] = {
            TOP_LINE: lambda ticket, num: num in ticket[0],
            MIDDLE_LINE: lambda ticket, num: num in ticket[1],
            BOTTOM_LINE: lambda ticket, num: num in ticket[2],
            FULL_HOUSE: lambda ticket, num: any(num in row for row in ticket),
            EARLY_FIVE: lambda ticket, num: any(num in row for row in ticket),
        }

    def validate_claim(
        self,
        ticket: List[List[Union[int, str]]],
        numbers_announced: List[int],
        claim_type: str,
    ) -> str:
        """
        Validates if a claim is valid based on the last number announced

        Args:
            ticket: 2D list representing 3x9 ticket
            numbers_announced: List of numbers announced so far
            claim_type: String - "top_line", "middle_line", "bottom_line", "full_house", "early_five"

        Returns:
            str: "Accepted" if claim is valid, "Rejected" otherwise
        """
        print(f"\nValidating claim for {claim_type}")
        print(f"Ticket state: {ticket}")
        print(f"Numbers announced: {numbers_announced}")

        # Validate ticket structure
        if (
            not ticket
            or len(ticket) != TICKET_ROW_SIZE
            or any(len(row) != TICKET_COLUMN_SIZE for row in ticket)
        ):
            print("Rejected: Invalid ticket structure")
            return REJECTED

        if not numbers_announced or claim_type not in self._claim_validators:
            print("Rejected: No numbers announced or invalid claim type")
            return REJECTED

        last_number = numbers_announced[-1]
        crossed_numbers = set(numbers_announced)
        print(f"Last number announced: {last_number}")
        print(f"Total crossed numbers: {crossed_numbers}")

        # Check if last number contributes to the win
        if not self._is_number_in_relevant_line(ticket, last_number, claim_type):
            print(f"Rejected: Last number {last_number} does not contribute to {claim_type}")
            return REJECTED

        validation_result = self._claim_validators[claim_type](ticket, crossed_numbers)
        print(f"Claim validation result: {'Accepted' if validation_result else 'Rejected'}")
        
        return ACCEPTED if validation_result else REJECTED

    def _is_number_in_relevant_line(
        self, ticket: List[List[Union[int, str]]], number: int, claim_type: str
    ) -> bool:
        """Checks if the last number announced contributes to the claimed win"""
        print(f"Checking if number {number} is in relevant line for {claim_type}")
        result = self._line_checkers[claim_type](ticket, number)
        print(f"Number {number} {'is' if result else 'is not'} in relevant line")
        return result
