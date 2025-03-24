def is_rectangle(commands):
    # Initialize position and directions
    x, y = 0, 0

    # Track the movement
    movements = []

    # Process all commands
    for cmd in commands:
        if cmd == "^":
            y += 1
            movements.append((0, 1))
        elif cmd == ">":
            x += 1
            movements.append((1, 0))
        elif cmd == "v":
            y -= 1
            movements.append((0, -1))
        elif cmd == "<":
            x -= 1
            movements.append((-1, 0))

    # Check if path is closed
    if x != 0 or y != 0:
        return False

    # Find direction changes
    directions = []
    current_dir = None

    for move in movements:
        if current_dir != move:
            directions.append(move)
            current_dir = move

    # A rectangle must have exactly 4 direction changes
    if len(directions) != 4:
        return False

    # Check perpendicular turns (for a rectangle, each turn should be 90 degrees)
    for i in range(4):
        dx1, dy1 = directions[i]
        dx2, dy2 = directions[(i + 1) % 4]

        # Dot product should be 0 for perpendicular vectors
        if dx1 * dx2 + dy1 * dy2 != 0:
            return False

    # Check if opposite sides have the same direction (but opposite orientation)
    dx1, dy1 = directions[0]
    dx3, dy3 = directions[2]

    dx2, dy2 = directions[1]
    dx4, dy4 = directions[3]

    if dx1 != -dx3 or dy1 != -dy3 or dx2 != -dx4 or dy2 != -dy4:
        return False

    return True


# Test cases
test1 = "^^^^>>>>vvvv<<<<"  # Perfect rectangle
test2 = "^>v<"  # Small square
test3 = "^^>>vv<<"  # Not a rectangle (not closed)
test4 = "^>v<^>v<"  # Double traversal of a square
test5 = "^>v<<"  # Not a rectangle (doesn't close properly)

print(f"Test 1: {is_rectangle(test1)}")  # True
print(f"Test 2: {is_rectangle(test2)}")  # True
print(f"Test 3: {is_rectangle(test3)}")  # False
print(f"Test 4: {is_rectangle(test4)}")  # False
print(f"Test 5: {is_rectangle(test5)}")  # False
