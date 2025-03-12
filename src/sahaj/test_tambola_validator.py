from tambola_validator import TambolaValidator
from tambola_consts import (
    TOP_LINE,
    MIDDLE_LINE,
    BOTTOM_LINE,
    FULL_HOUSE,
    EARLY_FIVE,
    EMPTY_CELL,
    ACCEPTED,
    REJECTED,
)


# Example usage
validator = TambolaValidator()


"""
Diagonal means 
00 - 00, 11, 21
01 - 12, 23


left 
04 - fro each row  - reduce -1 column and -1 row 
first cordinate 
on first cordinate reduce one more time 


right 
increase column 1 + increase row by 1 
increase column 2 + increase row by 2 

for middle row middle element 
last_element 
"""

# Test case 1 from readme
ticket = [
    [4, 16, "_", "_", 48, "_", 63, 76, "_"],
    [7, "_", 23, 38, "_", 52, "_", "_", 80],
    [9, "_", 25, "_", "_", 56, 64, "_", 83],
]
numbers_announced = [90, 4, 46, 63, 89, 16, 76, 48]
result = validator.validate_claim(ticket, numbers_announced, TOP_LINE)
print(f"Test case 1: {result}")  # Should print: Accepted

# Test case 2 from readme
numbers_announced = [90, 4, 46, 63, 89, 16, 76, 48, 12]
result = validator.validate_claim(ticket, numbers_announced, TOP_LINE)
print(f"Test case 2: {result}")  # Should print: Rejected


# Comprehensive test cases
def run_test_cases():
    validator = TambolaValidator()

    # Sample ticket for multiple tests
    ticket = [
        [4, 16, "_", "_", 48, "_", 63, 76, "_"],
        [7, "_", 23, 38, "_", 52, "_", "_", 80],
        [9, "_", 25, "_", "_", 56, 64, "_", 83],
    ]

    # Test case 1: Empty numbers_announced
    assert validator.validate_claim(ticket, [], TOP_LINE) == REJECTED, (
        "Test 1: Empty numbers - Expected: Rejected"
    )

    # Test case 2: Last number not contributing to win
    assert (
        validator.validate_claim(ticket, [4, 16, 48, 63, 76, 90], TOP_LINE) == REJECTED
    ), "Test 2: Last number not contributing - Expected: Rejected"

    # Test case 3: Valid top line
    assert (
        validator.validate_claim(ticket, [90, 4, 46, 63, 89, 16, 76, 48], TOP_LINE)
        == ACCEPTED
    ), "Test 3: Valid top line - Expected: Accepted"

    # Test case 4: Valid middle line
    assert (
        validator.validate_claim(ticket, [7, 23, 38, 52, 80], MIDDLE_LINE) == ACCEPTED
    ), "Test 4: Valid middle line - Expected: Accepted"

    # Test case 5: Valid bottom line
    assert (
        validator.validate_claim(ticket, [9, 25, 56, 64, 83], BOTTOM_LINE) == ACCEPTED
    ), "Test 5: Valid bottom line - Expected: Accepted"

    # Test case 6: Invalid claim type
    assert validator.validate_claim(ticket, [1, 2, 3], "invalid_type") == REJECTED, (
        "Test 6: Invalid claim type - Expected: Rejected"
    )

    # Test case 7: Early five with exactly 5 numbers
    assert (
        validator.validate_claim(ticket, [4, 16, 48, 63, 76], EARLY_FIVE) == ACCEPTED
    ), "Test 7: Valid early five - Expected: Accepted"

    # Test case 8: Early five with more than 5 numbers
    assert (
        validator.validate_claim(ticket, [4, 16, 48, 63, 76, 7], EARLY_FIVE) == ACCEPTED
    ), "Test 8: Early five with extra numbers - Expected: Accepted"

    # Test case 9: Early five with less than 5 numbers
    assert validator.validate_claim(ticket, [4, 16, 48, 63], EARLY_FIVE) == REJECTED, (
        "Test 9: Early five with less numbers - Expected: Rejected"
    )

    # Test case 10: Full house
    all_numbers = [num for row in ticket for num in row if num != EMPTY_CELL]
    assert validator.validate_claim(ticket, all_numbers, FULL_HOUSE) == ACCEPTED, (
        "Test 10: Valid full house - Expected: Accepted"
    )

    # Test case 11: Incomplete full house
    incomplete_numbers = all_numbers[:-1]
    assert (
        validator.validate_claim(ticket, incomplete_numbers, FULL_HOUSE) == REJECTED
    ), "Test 11: Incomplete full house - Expected: Rejected"

    # Test case 12: Last number matters for full house
    all_numbers_wrong_order = all_numbers[:-1] + [90]  # Last number not in ticket
    assert (
        validator.validate_claim(ticket, all_numbers_wrong_order, FULL_HOUSE)
        == REJECTED
    ), "Test 12: Full house with wrong last number - Expected: Rejected"

    # Test case 13: Empty ticket (completely empty list)
    empty_ticket = []
    assert validator.validate_claim(empty_ticket, [1, 2, 3], TOP_LINE) == REJECTED, (
        "Test 13: Empty ticket - Expected: Rejected"
    )

    # Test case 14: Ticket with empty rows
    empty_rows_ticket = [[], [], []]
    assert (
        validator.validate_claim(empty_rows_ticket, [1, 2, 3], TOP_LINE) == REJECTED
    ), "Test 14: Ticket with empty rows - Expected: Rejected"

    # Test case 15: Ticket with incorrect number of rows
    invalid_rows_ticket = [
        [4, 16, "_", "_", 48, "_", 63, 76, "_"],
        [7, "_", 23, 38, "_", 52, "_", "_", 80],
    ]  # Only 2 rows instead of 3
    assert (
        validator.validate_claim(invalid_rows_ticket, [4, 16, 48], TOP_LINE) == REJECTED
    ), "Test 15: Ticket with incorrect number of rows - Expected: Rejected"

    # Test case 16: Ticket with incorrect column count
    invalid_columns_ticket = [
        [4, 16, "_", "_", 48],  # Only 5 columns instead of 9
        [7, "_", 23, 38, "_"],
        [9, "_", 25, "_", "_"],
    ]
    assert (
        validator.validate_claim(invalid_columns_ticket, [4, 16, 48], TOP_LINE)
        == REJECTED
    ), "Test 16: Ticket with incorrect number of columns - Expected: Rejected"

    print("All test cases passed successfully!")


if __name__ == "__main__":
    run_test_cases()
