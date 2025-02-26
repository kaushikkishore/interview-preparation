## 10. Performance Testing

Performance testing ensures your code meets performance requirements and helps identify bottlenecks.

```python
import time
import statistics
import unittest
import matplotlib.pyplot as plt
import io
import sys
from contextlib import contextmanager

# Utility for capturing stdout/stderr
@contextmanager
def capture_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

# Functions to test
def slow_sort(items):
    """A deliberately inefficient sorting algorithm (bubble sort)"""
    items = items.copy()
    n = len(items)
    for i in range(n):
        for j in range(0, n - i - 1):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
    return items

def fast_sort(items):
    """Efficient sorting using Python's built-in sort"""
    return sorted(items.copy())

# Performance testing framework
class PerformanceTest:
    def __init__(self, name, setup=None):
        self.name = name
        self.setup = setup or (lambda: None)
        self.results = {}
    
    def measure_time(self, func, *args, **kwargs):
        """Measure execution time of a function"""
        # Run setup
        setup_data = self.setup()
        
        # If setup returns something, pass it as the first argument
        if setup_data is not None:
            args = (setup_data,) + args
        
        # Measure execution time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        return end_time - start_time, result
    
    def benchmark(self, func, iterations=10, *args, **kwargs):
        """Run a function multiple times and collect timing statistics"""
        times = []
        for _ in range(iterations):
            execution_time, _ = self.measure_time(func, *args, **kwargs)
            times.append(execution_time)
        
        stats = {
            'min': min(times),
            'max': max(times),
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0
        }
        
        self.results[func.__name__] = {
            'times': times,
            'stats': stats
        }
        
        return stats
    
    def compare(self, funcs, iterations=10, *args, **kwargs):
        """Compare multiple functions"""
        for func in funcs:
            stats = self.benchmark(func, iterations, *args, **kwargs)
            print(f"{func.__name__}:")
            print(f"  Mean time: {stats['mean']:.6f}s")
            print(f"  Median time: {stats['median']:.6f}s")
            print(f"  Min time: {stats['min']:.6f}s")
            print(f"  Max time: {stats['max']:.6f}s")
            print(f"  Std dev: {stats['stdev']:.6f}s")
            print()
    
    def plot_comparison(self, title="Performance Comparison"):
        """Plot comparison results"""
        if not self.results:
            raise ValueError("No benchmark results to plot")
        
        func_names = list(self.results.keys())
        means = [self.results[name]['stats']['mean'] for name in func_names]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(func_names, means)
        
        # Add labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.6f}s',
                    ha='center', va='bottom')
        
        plt.title(title)
        plt.ylabel('Mean Execution Time (seconds)')
        plt.xlabel('Function')
        plt.tight_layout()
        plt.show()

# Example usage of the performance testing framework
class TestSortingPerformance(unittest.TestCase):
    def setUp(self):
        import random
        # Create a list of 1000 random integers
        self.data = [random.randint(0, 1000) for _ in range(1000)]
    
    def test_sorting_performance(self):
        # Create test with setup function
        def setup():
            return self.data
        
        perf_test = PerformanceTest("Sorting Algorithms", setup)
        
        # Run benchmark with captured output
        with capture_output() as (out, err):
            perf_test.compare([slow_sort, fast_sort], iterations=5)
        
        # Check that fast_sort is significantly faster
        slow_mean = perf_test.results['slow_sort']['stats']['mean']
        fast_mean = perf_test.results['fast_sort']['stats']['mean']
        
        # fast_sort should be at least 10x faster for this size of input
        self.assertGreater(slow_mean / fast_mean, 10)
        
        # Print the comparison results
        print(out.getvalue())

# If run directly, perform a demo benchmark
if __name__ == "__main__":
    import random
    
    # Setup function that creates a random list
    def create_random_list(size=1000):
        return [random.randint(0, 1000) for _ in range(size)]
    
    # Test sorting performance with different input sizes
    for size in [100, 500, 1000, 2000]:
        print(f"Testing with list size: {size}")
        
        def setup():
            return create_random_list(size)
        
        perf_test = PerformanceTest(f"Sorting {size} items", setup)
        perf_test.compare([slow_sort, fast_sort], iterations=3)
        
        # Uncomment to show plot
        # perf_test.plot_comparison(f"Sorting Performance: {size} items")
        
        print("-" * 50)
```

## Interview Questions to Expect

1. "Describe your approach to unit testing in Python. How do you decide what to test and what not to test?"

2. "How would you test a function that depends on external APIs or services? What strategies would you use to make these tests reliable?"

3. "Explain the difference between unit tests, integration tests, and functional tests. When would you use each type?"

4. "What is mocking, and when would you use it in your tests? Can you provide an example?"

5. "How would you use property-based testing for a real-world problem? What are its advantages over traditional testing?"

6. "How do you ensure your test suite stays maintainable as your codebase grows?"

7. "Describe how you would implement a continuous integration pipeline for a Python project."

8. "What metrics do you use to evaluate the quality of your test suite? How do you know if your tests are good enough?"

9. "How would you approach testing a legacy application with little to no existing tests?"

10. "What strategies would you use to minimize test execution time in a large Python codebase?"

## Conclusion

Advanced testing and quality assurance practices are essential for building reliable and maintainable Python applications. Senior developers should be proficient in:

1. **Writing high-quality tests** - Understanding different testing approaches and knowing when to use each.

2. **Test-driven development** - Using tests to drive design and implementation.

3. **Mock testing** - Isolating components for focused testing.

4. **Property-based testing** - Testing properties and invariants rather than specific examples.

5. **Parameterized testing** - Testing multiple inputs efficiently.

6. **Test organization** - Using fixtures and factories to make tests maintainable.

7. **Continuous integration** - Automating test execution as part of the development workflow.

8. **Test coverage analysis** - Identifying untested code paths.

9. **Performance testing** - Ensuring code meets performance requirements.

By mastering these techniques, senior Python developers can build high-quality software that's reliable, maintainable, and performs well under real-world conditions.
# Advanced Python Testing and Quality Assurance

This document covers advanced testing and quality assurance techniques for senior Python developers with 10+ years of experience.

## 1. Mock Testing

Mock objects simulate the behavior of real objects in controlled ways, making them essential for isolating components during testing.

```python
import unittest
from unittest.mock import Mock, patch, MagicMock

# The code to test
class PaymentProcessor:
    def process_payment(self, amount, card_number):
        # In a real implementation, this would call an external payment API
        response = self._call_payment_api(amount, card_number)
        if response['status'] == 'success':
            return True
        return False
    
    def _call_payment_api(self, amount, card_number):
        # This would be a real API call in production
        # This is what we'll mock in our tests
        pass

# Tests with mocking
class TestPaymentProcessor(unittest.TestCase):
    def setUp(self):
        self.payment_processor = PaymentProcessor()
    
    def test_successful_payment(self):
        # Create a mock for the _call_payment_api method
        self.payment_processor._call_payment_api = Mock(
            return_value={'status': 'success', 'transaction_id': '123456'}
        )
        
        # Call the method being tested
        result = self.payment_processor.process_payment(100, '4111111111111111')
        
        # Assertions
        self.assertTrue(result)
        self.payment_processor._call_payment_api.assert_called_once_with(
            100, '4111111111111111'
        )
    
    def test_failed_payment(self):
        # Create a mock that returns a failure response
        self.payment_processor._call_payment_api = Mock(
            return_value={'status': 'failed', 'error': 'Insufficient funds'}
        )
        
        # Call the method being tested
        result = self.payment_processor.process_payment(100, '4111111111111111')
        
        # Assertions
        self.assertFalse(result)
        self.payment_processor._call_payment_api.assert_called_once()
    
    @patch('__main__.PaymentProcessor._call_payment_api')
    def test_with_patch_decorator(self, mock_api_call):
        # Configure the mock
        mock_api_call.return_value = {'status': 'success', 'transaction_id': '123456'}
        
        # Call the method
        result = self.payment_processor.process_payment(100, '4111111111111111')
        
        # Assertions
        self.assertTrue(result)
        mock_api_call.assert_called_once_with(100, '4111111111111111')

# If run directly, execute the tests
if __name__ == '__main__':
    unittest.main()
```

## 2. Property-Based Testing

Property-based testing focuses on testing properties that should always hold true, rather than specific examples.

```python
from hypothesis import given, strategies as st
import unittest

# Function to test
def sort_and_uniquify(items):
    """Sort a list and remove duplicates"""
    return sorted(set(items))

# Traditional unit tests
class TestSortAndUniquify(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(sort_and_uniquify([]), [])
    
    def test_single_item(self):
        self.assertEqual(sort_and_uniquify([5]), [5])
    
    def test_multiple_items(self):
        self.assertEqual(sort_and_uniquify([3, 1, 2]), [1, 2, 3])
    
    def test_duplicates(self):
        self.assertEqual(sort_and_uniquify([3, 1, 3, 2, 1]), [1, 2, 3])

# Property-based tests
class TestSortAndUniquifyProperties(unittest.TestCase):
    @given(st.lists(st.integers()))
    def test_result_contains_no_duplicates(self, items):
        result = sort_and_uniquify(items)
        # Check that no item appears twice
        self.assertEqual(len(result), len(set(result)))
    
    @given(st.lists(st.integers()))
    def test_result_is_sorted(self, items):
        result = sort_and_uniquify(items)
        # Check that the result is sorted
        self.assertEqual(result, sorted(result))
    
    @given(st.lists(st.integers()))
    def test_original_elements_are_preserved(self, items):
        result = sort_and_uniquify(items)
        # Check that all unique elements from the input are in the result
        self.assertEqual(set(result), set(items))
    
    @given(st.lists(st.integers()))
    def test_idempotent(self, items):
        # Applying the function twice should give the same result as once
        once = sort_and_uniquify(items)
        twice = sort_and_uniquify(once)
        self.assertEqual(once, twice)

# If run directly, execute the tests
if __name__ == '__main__':
    unittest.main()
```

## 3. Pytest Fixtures and Parameterization

Pytest offers powerful features for test organization, setup/teardown, and parameterization.

```python
import pytest
import tempfile
import os

# A simple user database class to test
class UserDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.users = {}
        self._load()
    
    def _load(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                for line in f:
                    if line.strip():
                        username, role = line.strip().split(',')
                        self.users[username] = role
    
    def save(self):
        with open(self.db_path, 'w') as f:
            for username, role in self.users.items():
                f.write(f"{username},{role}\n")
    
    def add_user(self, username, role):
        self.users[username] = role
        self.save()
    
    def get_user_role(self, username):
        return self.users.get(username)
    
    def delete_user(self, username):
        if username in self.users:
            del self.users[username]
            self.save()
            return True
        return False

# Fixtures for testing
@pytest.fixture
def temp_db_path():
    """Creates a temporary file for the database"""
    fd, path = tempfile.mkstemp()
    yield path
    os.close(fd)
    os.unlink(path)

@pytest.fixture
def empty_db(temp_db_path):
    """Creates an empty database"""
    db = UserDatabase(temp_db_path)
    return db

@pytest.fixture
def populated_db(empty_db):
    """Creates a database with some users"""
    empty_db.add_user("admin", "admin")
    empty_db.add_user("user1", "user")
    empty_db.add_user("guest", "guest")
    return empty_db

# Tests using fixtures
def test_empty_database(empty_db):
    assert empty_db.users == {}

def test_add_user(empty_db):
    empty_db.add_user("testuser", "user")
    assert empty_db.get_user_role("testuser") == "user"

def test_get_nonexistent_user(empty_db):
    assert empty_db.get_user_role("nonexistent") is None

def test_delete_user(populated_db):
    assert populated_db.delete_user("user1")
    assert populated_db.get_user_role("user1") is None

def test_delete_nonexistent_user(populated_db):
    assert not populated_db.delete_user("nonexistent")

# Parameterized tests
@pytest.mark.parametrize("username,role", [
    ("user1", "user"),
    ("admin", "admin"),
    ("guest", "guest")
])
def test_specific_users(populated_db, username, role):
    assert populated_db.get_user_role(username) == role

@pytest.mark.parametrize("invalid_input,expected", [
    (None, None),
    ("", None),
    (123, None)  # Non-string input
])
def test_get_user_with_invalid_input(populated_db, invalid_input, expected):
    assert populated_db.get_user_role(invalid_input) == expected
```

## 4. Integration Testing

Integration tests verify that different components work together correctly.

```python
import unittest
import tempfile
import os
import json

# Components to test
class UserRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                json.dump([], f)
    
    def find_by_id(self, user_id):
        with open(self.db_path, 'r') as f:
            users = json.load(f)
            for user in users:
                if user.get('id') == user_id:
                    return user
        return None
    
    def save(self, user):
        with open(self.db_path, 'r') as f:
            users = json.load(f)
        
        # Update or add user
        user_index = next((i for i, u in enumerate(users) if u.get('id') == user.get('id')), None)
        if user_index is not None:
            users[user_index] = user
        else:
            users.append(user)
        
        with open(self.db_path, 'w') as f:
            json.dump(users, f)
        
        return user

class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository
    
    def get_user(self, user_id):
        return self.user_repository.find_by_id(user_id)
    
    def create_user(self, user_data):
        if not user_data.get('name'):
            raise ValueError("User must have a name")
        
        return self.user_repository.save(user_data)
    
    def update_user_email(self, user_id, new_email):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            return None
        
        user['email'] = new_email
        return self.user_repository.save(user)

# Integration tests
class TestUserServiceIntegration(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for testing
        fd, self.db_path = tempfile.mkstemp()
        os.close(fd)
        
        # Initialize with test data
        with open(self.db_path, 'w') as f:
            json.dump([
                {"id": 1, "name": "John", "email": "john@example.com"},
                {"id": 2, "name": "Jane", "email": "jane@example.com"}
            ], f)
        
        # Set up the components
        self.user_repository = UserRepository(self.db_path)
        self.user_service = UserService(self.user_repository)
    
    def tearDown(self):
        # Clean up temporary file
        os.unlink(self.db_path)
    
    def test_get_existing_user(self):
        user = self.user_service.get_user(1)
        self.assertEqual(user['name'], "John")
        self.assertEqual(user['email'], "john@example.com")
    
    def test_get_nonexistent_user(self):
        user = self.user_service.get_user(999)
        self.assertIsNone(user)
    
    def test_create_user(self):
        new_user = {"id": 3, "name": "Bob", "email": "bob@example.com"}
        created_user = self.user_service.create_user(new_user)
        
        # Verify the user was created
        self.assertEqual(created_user['name'], "Bob")
        
        # Verify the user is in the repository
        retrieved_user = self.user_service.get_user(3)
        self.assertEqual(retrieved_user['email'], "bob@example.com")
    
    def test_create_user_without_name(self):
        invalid_user = {"id": 4, "email": "invalid@example.com"}
        with self.assertRaises(ValueError):
            self.user_service.create_user(invalid_user)
    
    def test_update_user_email(self):
        updated_user = self.user_service.update_user_email(2, "new.jane@example.com")
        
        # Verify the update was successful
        self.assertEqual(updated_user['email'], "new.jane@example.com")
        
        # Verify the update is persistent
        retrieved_user = self.user_service.get_user(2)
        self.assertEqual(retrieved_user['email'], "new.jane@example.com")

if __name__ == '__main__':
    unittest.main()
```

## 5. Test-Driven Development (TDD)

TDD involves writing tests before implementing functionality, following the "Red-Green-Refactor" cycle.

```python
import unittest

# Step 1: Write the test first (Red phase)
class TestShoppingCart(unittest.TestCase):
    def test_empty_cart_total(self):
        cart = ShoppingCart()
        self.assertEqual(cart.total(), 0)
    
    def test_add_item_to_cart(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 2)
        self.assertEqual(cart.total(), 2.0)
    
    def test_add_multiple_items(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 2)
        cart.add_item("banana", 0.5, 3)
        self.assertEqual(cart.total(), 3.5)
    
    def test_remove_item(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 2)
        cart.remove_item("apple")
        self.assertEqual(cart.total(), 0)
    
    def test_apply_discount(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 10)
        cart.apply_discount(10)  # 10% discount
        self.assertEqual(cart.total(), 9.0)

# Step 2: Implement the code to make tests pass (Green phase)
class ShoppingCart:
    def __init__(self):
        self.items = {}
        self.discount = 0
    
    def add_item(self, item_name, price, quantity=1):
        self.items[item_name] = {
            'price': price,
            'quantity': quantity
        }
    
    def remove_item(self, item_name):
        if item_name in self.items:
            del self.items[item_name]
    
    def apply_discount(self, discount_percent):
        self.discount = discount_percent
    
    def total(self):
        subtotal = sum(
            item['price'] * item['quantity']
            for item in self.items.values()
        )
        discount_amount = subtotal * (self.discount / 100)
        return subtotal - discount_amount

# Step 3: Refactor the code while keeping tests passing
class RefactoredShoppingCart:
    def __init__(self):
        self.items = {}
        self.discount_strategy = NoDiscount()
    
    def add_item(self, item_name, price, quantity=1):
        if item_name in self.items:
            self.items[item_name]['quantity'] += quantity
        else:
            self.items[item_name] = {
                'price': price,
                'quantity': quantity
            }
    
    def remove_item(self, item_name):
        if item_name in self.items:
            del self.items[item_name]
    
    def apply_discount(self, discount_percent):
        self.discount_strategy = PercentageDiscount(discount_percent)
    
    def total(self):
        subtotal = sum(
            item['price'] * item['quantity']
            for item in self.items.values()
        )
        return self.discount_strategy.apply(subtotal)

# Discount strategies
class NoDiscount:
    def apply(self, amount):
        return amount

class PercentageDiscount:
    def __init__(self, percent):
        self.percent = percent
    
    def apply(self, amount):
        return amount * (1 - self.percent / 100)

# Additional tests for refactored implementation
class TestRefactoredShoppingCart(unittest.TestCase):
    def test_add_same_item_multiple_times(self):
        cart = RefactoredShoppingCart()
        cart.add_item("apple", 1.0, 2)
        cart.add_item("apple", 1.0, 3)  # Should update quantity, not add duplicate
        self.assertEqual(cart.total(), 5.0)
    
    def test_fixed_amount_discount(self):
        cart = RefactoredShoppingCart()
        cart.add_item("apple", 1.0, 10)
        
        # Custom discount strategy
        class FixedDiscount:
            def __init__(self, amount):
                self.amount = amount
            
            def apply(self, subtotal):
                return max(0, subtotal - self.amount)
        
        cart.discount_strategy = FixedDiscount(2.0)
        self.assertEqual(cart.total(), 8.0)

if __name__ == '__main__':
    unittest.main()
```

## 6. Test Coverage Analysis

Test coverage measures how much of your code is executed during tests, helping identify untested code paths.

```python
"""
# This is an example of using coverage.py to measure test coverage

# Installation:
# pip install coverage

# Basic usage:
# 1. Run tests with coverage:
#    coverage run -m unittest discover

# 2. Generate a report:
#    coverage report -m

# 3. Generate HTML report (more detailed):
#    coverage html

# Example .coveragerc file for configuration:
[run]
source = my_package
omit = 
    */tests/*
    */migrations/*
    */__init__.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:
    pass
    raise ImportError

[html]
directory = coverage_html
"""

# Example code to be tested (in my_package/calculator.py)
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def complex_function(x, y, operation='add'):
    """Complex function with multiple branches"""
    if operation == 'add':
        result = add(x, y)
    elif operation == 'subtract':
        result = subtract(x, y)
    elif operation == 'multiply':
        result = multiply(x, y)
    elif operation == 'divide':
        result = divide(x, y)
    else:
        raise ValueError(f"Unknown operation: {operation}")
    
    if result < 0:
        return "Negative result"
    elif result == 0:
        return "Zero result"
    else:
        return "Positive result"

# Example tests (in tests/test_calculator.py)
import unittest
from my_package.calculator import add, subtract, multiply, divide, complex_function

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(-1, 1), 0)
    
    def test_subtract(self):
        self.assertEqual(subtract(3, 2), 1)
        self.assertEqual(subtract(5, 10), -5)
    
    def test_multiply(self):
        self.assertEqual(multiply(3, 2), 6)
        self.assertEqual(multiply(-1, -1), 1)
    
    def test_divide(self):
        self.assertEqual(divide(6, 2), 3)
        self.assertEqual(divide(5, 2), 2.5)
        
        with self.assertRaises(ValueError):
            divide(1, 0)
    
    def test_complex_function_add(self):
        self.assertEqual(complex_function(5, 3, 'add'), "Positive result")
    
    def test_complex_function_negative(self):
        self.assertEqual(complex_function(1, 5, 'subtract'), "Negative result")
    
    # Missing test for complex_function with 'zero result'
    # Missing test for complex_function with 'multiply'
    # Missing test for complex_function with 'divide'
    # Missing test for complex_function with invalid operation
```

## 7. Behavior-Driven Development (BDD)

BDD focuses on describing behavior in natural language, then implementing tests to verify that behavior.

```python
"""
# Example using behave for BDD testing
# Installation: pip install behave

# Features are written in Gherkin syntax (in features/calculator.feature)
Feature: Calculator
  As a user
  I want to perform basic arithmetic operations
  So that I can do calculations

  Scenario: Addition
    Given I have entered 5 into the calculator
    And I have entered 7 into the calculator
    When I press add
    Then the result should be 12 on the screen

  Scenario: Division
    Given I have entered 10 into the calculator
    And I have entered 2 into the calculator
    When I press divide
    Then the result should be 5 on the screen

  Scenario: Division by zero
    Given I have entered 10 into the calculator
    And I have entered 0 into the calculator
    When I press divide
    Then the calculator should display an error

# Step implementations (in features/steps/calculator_steps.py)
from behave import given, when, then
from calculator import Calculator

@given('I have entered {number:d} into the calculator')
def step_impl(context, number):
    if not hasattr(context, 'calculator'):
        context.calculator = Calculator()
    if not hasattr(context, 'numbers'):
        context.numbers = []
    context.numbers.append(number)

@when('I press add')
def step_impl(context):
    context.result = context.calculator.add(context.numbers[0], context.numbers[1])

@when('I press divide')
def step_impl(context):
    try:
        context.result = context.calculator.divide(context.numbers[0], context.numbers[1])
        context.error = None
    except ValueError as e:
        context.error = str(e)

@then('the result should be {result:d} on the screen')
def step_impl(context, result):
    assert context.result == result, f"Expected {result}, got {context.result}"

@then('the calculator should display an error')
def step_impl(context):
    assert context.error is not None, "Expected an error, but none occurred"
"""

# Simple calculator implementation for the BDD example
class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
```

## 8. Continuous Integration Testing

Continuous Integration (CI) automatically runs tests when code changes are pushed, ensuring code quality.

```yaml
# Example GitHub Actions workflow (.github/workflows/python-tests.yml)
name: Python Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10']

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    
    - name: Lint with flake8
      run: |
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics
    
    - name: Check type hints with mypy
      run: |
        mypy .
    
    - name: Run unit tests
      run: |
        pytest tests/unit
    
    - name: Run integration tests
      run: |
        pytest tests/integration
    
    - name: Generate coverage report
      run: |
        pytest --cov=./ --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

## 9. Test Fixtures and Factories

Test fixtures and factories help create test data in a maintainable way.

```python
import pytest
import random
import string
from datetime import datetime, timedelta

# Entity classes
class User:
    def __init__(self, id=None, username=None, email=None, created_at=None, is_active=True):
        self.id = id
        self.username = username
        self.email = email
        self.created_at = created_at or datetime.now()
        self.is_active = is_active
    
    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}')"

class Order:
    def __init__(self, id=None, user=None, items=None, total=0.0, created_at=None):
        self.id = id
        self.user = user
        self.items = items or []
        self.total = total
        self.created_at = created_at or datetime.now()
    
    def __repr__(self):
        return f"Order(id={self.id}, user={self.user.id if self.user else None}, items={len(self.items)})"

class OrderItem:
    def __init__(self, id=None, order=None, product_name=None, quantity=1, price=0.0):
        self.id = id
        self.order = order
        self.product_name = product_name
        self.quantity = quantity
        self.price = price
    
    @property
    def subtotal(self):
        return self.quantity * self.price
    
    def __repr__(self):
        return f"OrderItem(id={self.id}, product='{self.product_name}', quantity={self.quantity})"

# Factory class for generating test data
class Factory:
    _id_counter = 0
    
    @classmethod
    def get_next_id(cls):
        cls._id_counter += 1
        return cls._id_counter
    
    @classmethod
    def random_string(cls, length=10):
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    @classmethod
    def create_user(cls, **kwargs):
        """Create a user with default or specified attributes"""
        defaults = {
            'id': cls.get_next_id(),
            'username': f"user_{cls.random_string(5)}",
            'email': f"{cls.random_string(8)}@example.com",
            'created_at': datetime.now() - timedelta(days=random.randint(1, 365)),
            'is_active': True
        }
        # Override defaults with provided kwargs
        defaults.update(kwargs)
        return User(**defaults)
    
    @classmethod
    def create_order(cls, user=None, num_items=None, **kwargs):
        """Create an order with default or specified attributes"""
        if user is None:
            user = cls.create_user()
        
        defaults = {
            'id': cls.get_next_id(),
            'user': user,
            'created_at': datetime.now() - timedelta(days=random.randint(0, 30))
        }
        
        # Override defaults with provided kwargs
        defaults.update(kwargs)
        order = Order(**defaults)
        
        # Add items to the order if requested
        if num_items:
            items = []
            total = 0.0
            for _ in range(num_items):
                item = cls.create_order_item(order=order)
                items.append(item)
                total += item.subtotal
            
            order.items = items
            order.total = total
        
        return order
    
    @classmethod
    def create_order_item(cls, order=None, **kwargs):
        """Create an order item with default or specified attributes"""
        defaults = {
            'id': cls.get_next_id(),
            'order': order,
            'product_name': f"Product {cls.random_string(8)}",
            'quantity': random.randint(1, 5),
            'price': round(random.uniform(5.0, 100.0), 2)
        }
        
        # Override defaults with provided kwargs
        defaults.update(kwargs)
        return OrderItem(**defaults)

# Example pytest fixtures using the factory
@pytest.fixture
def user():
    """Returns a standard user"""
    return Factory.create_user()

@pytest.fixture
def admin_user():
    """Returns an admin user"""
    return Factory.create_user(username="admin", email="admin@example.com")

@pytest.fixture
def order_with_items(user):
    """Returns an order with 3 items"""
    return Factory.create_order(user=user, num_items=3)

# Example tests using fixtures and factories
def test_order_total(order_with_items):
    """Test that the order total matches the sum of item subtotals"""
    expected_total = sum(item.subtotal for item in order_with_items.items)
    assert order_with_items.total == expected_total

def test_create_custom_order():
    """Test creating a custom order with the factory"""
    user = Factory.create_user(username="testuser")
    order = Factory.create_order(
        user=user,
        created_at=datetime(2023, 1, 1)
    )
    
    # Add specific items
    item1 = Factory.create_order_item(order=order, product_name="Laptop", quantity=1, price=1200.0)
    item2 = Factory.create_order_item(order=order, product_name="Mouse", quantity=2, price=25.0)
    
    order.items = [item1, item2]
    order.total = item1.subtotal + item2.subtotal
    
    assert order.user.username == "testuser"
    assert len(order.items) == 2
    assert order.total == 1250.0
    assert order.created_at == datetime(2023, 1, 1)