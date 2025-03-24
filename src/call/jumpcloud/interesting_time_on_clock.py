"""
Problem Description:
You are given two strings representing times of a day in the format 'HH:MM:SS', where:
- 'HH' is a two-digit number from 00 to 23, representing the hour
- 'MM' is a two-digit number from 00 to 59, representing the minute
- 'SS' is a two-digit number from 00 to 59, representing the second

A time is considered "interesting" if it uses at most 2 distinct digits when written in the format 'HH:MM:SS'.
For example, '15:15:15' is interesting because it only uses one distinct digit ('1' and '5').
Another example is '22:22:00' which is interesting because it only uses two distinct digits ('0' and '2').

Given two times S and T, your task is to count how many interesting times occur from S to T (inclusive).

Example:
- For S = "15:15:00" and T = "15:15:12", there are 3 interesting times: "15:15:00", "15:15:05", "15:15:11"

Constraints:
- S and T are valid times in the format 'HH:MM:SS'
- S occurs before or at the same time as T on the same day
"""


def solution(S, T):
    # Convert time strings to seconds since midnight
    def time_to_seconds(time_str):
        h, m, s = map(int, time_str.split(":"))
        return h * 3600 + m * 60 + s

    # Convert seconds to time string format "HH:MM:SS"
    def seconds_to_time(seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    # Check if a time is interesting (uses at most 2 distinct digits)
    def is_interesting(time_str):
        # Remove colons and count distinct digits
        digits = time_str.replace(":", "")
        return len(set(digits)) <= 2

    # Convert input times to seconds
    start_seconds = time_to_seconds(S)
    end_seconds = time_to_seconds(T)

    # Count interesting times
    count = 0
    for seconds in range(start_seconds, end_seconds + 1):
        time_str = seconds_to_time(seconds)
        if is_interesting(time_str):
            count += 1

    return count


# Test cases
def test_solution():
    test_cases = [
        {
            "S": "15:15:00",
            "T": "15:15:12",
            "expected": 1,  # Only 15:15:11 has at most 2 distinct digits (1 and 5)
            "description": "Small range with only one interesting time",
        },
        {
            "S": "22:22:21",
            "T": "22:22:23",
            "expected": 3,  # All three times have only digits 1, 2
            "description": "All times in range are interesting (only digits 1, 2)",
        },
        {
            "S": "00:00:00",
            "T": "00:00:10",
            "expected": 11,  # All times from 00:00:00 to 00:00:10 have at most 2 distinct digits
            "description": "All times with 0s and single other digit are interesting",
        },
        {
            "S": "12:34:56",
            "T": "12:34:56",
            "expected": 0,  # This time has 6 distinct digits (1,2,3,4,5,6)
            "description": "Single time point with more than 2 distinct digits",
        },
        {
            "S": "11:11:11",
            "T": "11:11:11",
            "expected": 1,  # This time has only 1 distinct digit
            "description": "Single time point with only 1 distinct digit",
        },
    ]

    for i, test in enumerate(test_cases):
        result = solution(test["S"], test["T"])
        passed = result == test["expected"]
        status = "PASSED" if passed else "FAILED"
        print(f"Test {i + 1} ({test['description']}): {status}")
        if not passed:
            print(f"  Input: S={test['S']}, T={test['T']}")
            print(f"  Expected: {test['expected']}, Got: {result}")


if __name__ == "__main__":
    test_solution()
