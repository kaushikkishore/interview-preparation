# Advanced Python Concepts for Senior Developers - Part 2

This document covers two more advanced Python concepts essential for senior developers with 10+ years of experience.

## 4. Advanced Design Patterns

Design patterns provide proven solutions to common programming problems, especially important in large codebases.

### Dependency Injection

```python
# Interfaces (using abstract base classes)
from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def query(self, sql):
        pass
    
    @abstractmethod
    def execute(self, sql, params=None):
        pass

class CacheInterface(ABC):
    @abstractmethod
    def get(self, key):
        pass
    
    @abstractmethod
    def set(self, key, value, ttl=None):
        pass

class LoggerInterface(ABC):
    @abstractmethod
    def log(self, level, message):
        pass

# Implementations
class PostgresDatabase(DatabaseInterface):
    def query(self, sql):
        print(f"PostgreSQL query: {sql}")
        return [{"id": 1, "name": "Test User"}]
    
    def execute(self, sql, params=None):
        params_str = str(params) if params else "None"
        print(f"PostgreSQL execute: {sql} with params {params_str}")
        return True

class RedisCache(CacheInterface):
    def __init__(self):
        self._cache = {}
    
    def get(self, key):
        print(f"Redis getting: {key}")
        return self._cache.get(key)
    
    def set(self, key, value, ttl=None):
        print(f"Redis setting: {key} to {value}" + (f" with TTL {ttl}s" if ttl else ""))
        self._cache[key] = value

class ConsoleLogger(LoggerInterface):
    def log(self, level, message):
        print(f"[{level.upper()}] {message}")

# Service with injected dependencies
class UserService:
    def __init__(self, database, cache, logger):
        self.db = database
        self.cache = cache
        self.logger = logger
    
    def get_user(self, user_id):
        # Try cache first
        cache_key = f"user:{user_id}"
        cached_user = self.cache.get(cache_key)
        
        if cached_user:
            self.logger.log("info", f"Cache hit for user {user_id}")
            return cached_user
        
        # Query database
        self.logger.log("info", f"Cache miss for user {user_id}, querying database")
        user = self.db.query(f"SELECT * FROM users WHERE id = {user_id}")
        
        if user:
            # Update cache
            self.cache.set(cache_key, user[0], ttl=300)
            return user[0]
        
        return None

# Usage
if __name__ == "__main__":
    # Create dependencies
    db = PostgresDatabase()
    cache = RedisCache()
    logger = ConsoleLogger()
    
    # Create service with dependencies injected
    user_service = UserService(db, cache, logger)
    
    # Use the service
    print("\nFirst request (cache miss):")
    user = user_service.get_user(1)
    print(f"Got user: {user}")
    
    print("\nSecond request (cache hit):")
    user = user_service.get_user(1)
    print(f"Got user: {user}")
```

### Context Managers

```python
class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
    
    def connect(self):
        print(f"Connecting to database: {self.connection_string}")
        self.connection = {"status": "connected"}
        return self.connection
    
    def disconnect(self):
        print("Disconnecting from database")
        self.connection = None
    
    def execute(self, query):
        if not self.connection:
            raise RuntimeError("Not connected to database")
        print(f"Executing query: {query}")
        return [{"result": "data"}]

class TransactionContext:
    def __init__(self, db):
        self.db = db
        
    def __enter__(self):
        print("Starting transaction")
        self.db.execute("BEGIN TRANSACTION")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("Committing transaction")
            self.db.execute("COMMIT")
        else:
            print(f"Rolling back transaction due to {exc_type.__name__}: {exc_val}")
            self.db.execute("ROLLBACK")
        return False  # Don't suppress exceptions

# Usage
db = DatabaseConnection("postgres://localhost/testdb")
db.connect()

# Successful transaction
with TransactionContext(db):
    db.execute("INSERT INTO users (name) VALUES ('John')")
    db.execute("UPDATE users SET status = 'active' WHERE name = 'John'")

# Failed transaction
try:
    with TransactionContext(db):
        db.execute("INSERT INTO users (name) VALUES ('Jane')")
        # Simulate an error
        raise ValueError("Something went wrong")
        db.execute("This won't execute")
except ValueError:
    print("Caught the error outside the context manager")

db.disconnect()
```

### Singleton Pattern (Thread-safe)

```python
import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                print(f"Creating new {cls.__name__} instance")
                cls._instance = super().__new__(cls)
                # Initialize the instance
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self, value=None):
        # Only initialize once
        with self._lock:
            if not getattr(self, '_initialized', False):
                print(f"Initializing with value: {value}")
                self.value = value
                self._initialized = True

# Usage in multiple threads
def create_singleton(value, results):
    instance = Singleton(value)
    results.append((threading.current_thread().name, instance, instance.value))

if __name__ == "__main__":
    # Test in multiple threads
    threads = []
    results = []
    
    for i in range(5):
        thread = threading.Thread(target=create_singleton, args=(i, results))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Show results
    for thread_name, instance, value in results:
        print(f"Thread {thread_name}: instance at {hex(id(instance))}, value = {value}")
    
    # Verify singleton behavior
    instances = [instance for _, instance, _ in results]
    first_instance = instances[0]
    all_same = all(instance is first_instance for instance in instances)
    print(f"All instances are the same object: {all_same}")
    print(f"The value is from the first initialization: {first_instance.value == 0}")
```

### Observer Pattern

```python
class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
    
    def notify(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(self, *args, **kwargs)

class Observer:
    def update(self, subject, *args, **kwargs):
        pass

# Example implementation
class DataSource(Subject):
    def __init__(self):
        super().__init__()
        self._data = None
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        self._data = value
        self.notify(data=value)

class DataLogger(Observer):
    def __init__(self, name):
        self.name = name
    
    def update(self, subject, *args, **kwargs):
        print(f"Logger {self.name} received: {kwargs.get('data')}")

class DataAnalyzer(Observer):
    def update(self, subject, *args, **kwargs):
        data = kwargs.get('data')
        if isinstance(data, (int, float)):
            print(f"Analyzer: value {data} is {'even' if data % 2 == 0 else 'odd'}")
        else:
            print(f"Analyzer: received {data} (not a number)")

# Usage
data_source = DataSource()

logger1 = DataLogger("Main")
logger2 = DataLogger("Backup")
analyzer = DataAnalyzer()

data_source.attach(logger1)
data_source.attach(logger2)
data_source.attach(analyzer)

# Updates will be sent to all observers
data_source.data = 10
data_source.data = 15

# Detach one observer
data_source.detach(logger2)

# Only remaining observers will be notified
data_source.data = "test"
```

## 5. Performance Optimization

Optimizing Python code requires understanding memory usage, CPU utilization, and algorithmic efficiency.

### Memory-Efficient Processing with Generators

```python
import sys
import time
import os

def get_memory_usage():
    """Return memory usage in MB"""
    import psutil
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / (1024 * 1024)  # Convert to MB
    return mem

# Inefficient approach (loads everything into memory)
def read_and_process_inefficient(filename, n=1000000):
    print("Creating test file...")
    # Create a test file
    with open(filename, 'w') as f:
        for i in range(n):
            f.write(f"Line {i}\n")
    
    print("\nInefficient approach (loading entire file):")
    start_time = time.time()
    start_mem = get_memory_usage()
    
    # Load entire file into memory
    with open(filename) as f:
        lines = f.readlines()
    
    # Process each line
    results = []
    for line in lines:
        # Simulate processing
        processed = line.strip().upper()
        results.append(processed)
    
    end_time = time.time()
    end_mem = get_memory_usage()
    
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    print(f"Memory used: {end_mem - start_mem:.2f} MB")
    print(f"First 3 results: {results[:3]}")
    return len(results)

# Efficient approach (using generators)
def read_and_process_efficient(filename):
    print("\nEfficient approach (using generators):")
    start_time = time.time()
    start_mem = get_memory_usage()
    
    # Process line by line without loading entire file
    def process_lines():
        with open(filename) as f:
            for i, line in enumerate(f):
                # Simulate processing
                yield line.strip().upper()
                if i % 1000000 == 0 and i > 0:
                    print(f"Processed {i} lines so far")
    
    # Create generator and process results
    results_generator = process_lines()
    
    # Only store the count, not all results
    count = 0
    first_results = []
    for i, result in enumerate(results_generator):
        count += 1
        if i < 3:
            first_results.append(result)
    
    end_time = time.time()
    end_mem = get_memory_usage()
    
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    print(f"Memory used: {end_mem - start_mem:.2f} MB")
    print(f"First 3 results: {first_results}")
    return count

if __name__ == "__main__":
    filename = "test_data.txt"
    
    # Run inefficient approach
    count1 = read_and_process_inefficient(filename)
    
    # Run efficient approach
    count2 = read_and_process_efficient(filename)
    
    # Verify both approaches processed the same number of lines
    print(f"\nBoth approaches processed {count1} lines")
    assert count1 == count2, "Line counts don't match!"
    
    # Clean up
    os.remove(filename)
```

### Memoization and Caching

```python
import time
import functools

# Fibonacci without memoization
def fibonacci_slow(n):
    if n <= 1:
        return n
    return fibonacci_slow(n-1) + fibonacci_slow(n-2)

# Fibonacci with manual memoization
def fibonacci_manual_memo():
    cache = {}
    
    def fib(n):
        if n in cache:
            return cache[n]
        if n <= 1:
            result = n
        else:
            result = fib(n-1) + fib(n-2)
        cache[n] = result
        return result
    
    return fib

# Fibonacci with lru_cache
@functools.lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n-1) + fibonacci_lru(n-2)

def benchmark_fibonacci(n):
    print(f"Benchmarking Fibonacci({n})")
    
    # Slow version (only for small n)
    if n <= 30:
        start = time.time()
        result = fibonacci_slow(n)
        duration = time.time() - start
        print(f"Without memoization: {duration:.4f} seconds, result: {result}")
    else:
        print("Skipping non-memoized version (would take too long)")
    
    # Manual memoization
    start = time.time()
    fib = fibonacci_manual_memo()
    result = fib(n)
    duration = time.time() - start
    print(f"With manual memoization: {duration:.4f} seconds, result: {result}")
    
    # Using lru_cache
    start = time.time()
    result = fibonacci_lru(n)
    duration = time.time() - start
    print(f"With lru_cache: {duration:.4f} seconds, result: {result}")

# Custom caching class with TTL (Time To Live)
class TtlCache:
    def __init__(self, ttl_seconds=60):
        self.cache = {}
        self.ttl = ttl_seconds
    
    def cached(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            current_time = time.time()
            
            # Check if result is cached and not expired
            if key in self.cache:
                result, timestamp = self.cache[key]
                if current_time - timestamp < self.ttl:
                    print(f"Cache hit for {func.__name__}{args}")
                    return result
            
            # Call the function and cache result
            print(f"Cache miss for {func.__name__}{args}")
            result = func(*args, **kwargs)
            self.cache[key] = (result, current_time)
            return result
        
        return wrapper

# Usage
cache = TtlCache(ttl_seconds=5)

@cache.cached
def expensive_operation(x, y):
    print(f"Performing expensive operation with {x}, {y}")
    time.sleep(1)  # Simulate expensive computation
    return x * y

def test_ttl_cache():
    print("\nTesting TTL Cache:")
    
    # First call (cache miss)
    result1 = expensive_operation(5, 7)
    print(f"Result: {result1}")
    
    # Second call (cache hit)
    result2 = expensive_operation(5, 7)
    print(f"Result: {result2}")
    
    # Different parameters (cache miss)
    result3 = expensive_operation(10, 20)
    print(f"Result: {result3}")
    
    # Wait for TTL to expire
    print("Waiting for cache to expire...")
    time.sleep(6)
    
    # After TTL expired (cache miss)
    result4 = expensive_operation(5, 7)
    print(f"Result: {result4}")

if __name__ == "__main__":
    # Benchmark different Fibonacci implementations
    benchmark_fibonacci(35)
    
    # Test TTL cache
    test_ttl_cache()
```

### Code Profiling

```python
import cProfile
import pstats
import io
import random

def slow_function():
    total = 0
    for i in range(1000000):
        total += i
    return total

def medium_function():
    return sum(random.randint(1, 100) for _ in range(10000))

def fast_function():
    return sum(range(1000))

def combined_function():
    a = slow_function()
    b = medium_function()
    c = fast_function()
    return a + b + c

def profile_function(func, sort_by='cumulative'):
    """Profile a function and print stats"""
    # Create a profiler
    pr = cProfile.Profile()
    
    # Run the function within the profiler
    pr.enable()
    result = func()
    pr.disable()
    
    # Print stats
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
    ps.print_stats(10)  # Print top 10 entries
    
    print(s.getvalue())
    return result

if __name__ == "__main__":
    print("Profiling combined_function:")
    profile_function(combined_function)
    
    print("\nProfiling with different sort orders:")
    profile_function(combined_function, sort_by='time')
```

## Interview Questions to Expect

1. "How do you implement a thread-safe singleton pattern in Python?"
2. "Explain the advantages of dependency injection and how you would implement it in a Python application."
3. "Describe a situation where you used custom context managers to simplify resource management."
4. "What techniques would you use to optimize a Python application that's processing large files?"
5. "How would you implement caching in a Python application? What considerations should be made for TTL and invalidation?"
6. "When would you use a generator instead of a list, and what are the performance implications?"