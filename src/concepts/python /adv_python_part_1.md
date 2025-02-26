# Advanced Python Concepts for Senior Developers - Part 1

This document covers three advanced Python concepts essential for senior developers with 10+ years of experience, with explanations and practical code examples for each topic.

## 1. Advanced Memory Management

Python handles memory automatically, but understanding its memory model is crucial for optimizing large applications and preventing memory leaks.

### Reference Counting and Garbage Collection

Python uses reference counting as its primary memory management mechanism, complemented by a cyclic garbage collector.

```python
import sys
import gc

# Example showing reference counting
lst = [1, 2, 3]  # Create a list
print(f"Initial reference count: {sys.getrefcount(lst) - 1}")  # -1 for the getrefcount parameter

# Create another reference to the same list
lst2 = lst
print(f"After another reference: {sys.getrefcount(lst) - 1}")

# Remove one reference
lst2 = None
print(f"After removing reference: {sys.getrefcount(lst) - 1}")

# Check garbage collection thresholds
print(f"GC thresholds: {gc.get_threshold()}")
```

### Weak References

Weak references are references that don't increase an object's reference count, useful for caching and preventing memory leaks in circular references.

```python
import weakref

class ExpensiveObject:
    def __init__(self, value):
        self.value = value
    
    def __del__(self):
        print(f"Deleting object with value: {self.value}")

class CachingSystem:
    def __init__(self):
        self._cache = {}
        self._refs = {}
    
    def cache_item(self, key, value):
        # Store the actual object in the cache
        self._cache[key] = value
        # Store a weak reference that won't prevent garbage collection
        self._refs[key] = weakref.ref(value, lambda _: self._cache.pop(key, None))
    
    def get_item(self, key):
        return self._cache.get(key)

# Usage example
cache = CachingSystem()
obj = ExpensiveObject("important data")

# Cache the object
cache.cache_item("key1", obj)
print(f"Object in cache: {cache.get_item('key1').value}")

# When the only remaining reference to the object is removed,
# it will be garbage collected despite being in the cache
obj = None
# Force garbage collection to demonstrate the effect
gc.collect()
print(f"Object after deletion: {cache.get_item('key1')}")  # Will be None
```

### Memory Profiling

```python
import tracemalloc
import random

def allocate_memory():
    # Create a large list
    return [random.random() for _ in range(1000000)]

# Start tracking memory allocations
tracemalloc.start()

# Take a snapshot before allocation
snapshot1 = tracemalloc.take_snapshot()

# Allocate memory
large_list = allocate_memory()

# Take a snapshot after allocation
snapshot2 = tracemalloc.take_snapshot()

# Compare snapshots
top_stats = snapshot2.compare_to(snapshot1, 'lineno')

print("[ Top 5 memory differences ]")
for stat in top_stats[:5]:
    print(stat)
```

## 2. Metaprogramming and Descriptors

Metaprogramming is the practice of writing code that manipulates code. Python's dynamic nature allows powerful metaprogramming techniques.

### Descriptors

Descriptors control attribute access and are the foundation for properties, methods, and class methods.

```python
class TypedProperty:
    def __init__(self, name, property_type, default=None):
        self.name = f"_{name}"
        self.property_type = property_type
        self.default = default
        
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name, self.default)
        
    def __set__(self, instance, value):
        if not isinstance(value, self.property_type):
            raise TypeError(f"Expected {self.property_type}, got {type(value)}")
        setattr(instance, self.name, value)

class Person:
    name = TypedProperty("name", str)
    age = TypedProperty("age", int)
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Usage
try:
    # This works
    person = Person("John", 30)
    print(f"Person: {person.name}, {person.age} years old")
    
    # This raises TypeError
    person.age = "thirty"
except TypeError as e:
    print(f"Error: {e}")
```

### Metaclasses

Metaclasses customize class creation, allowing for patterns like registry, automatic method decoration, and validation.

```python
class ServiceMeta(type):
    def __new__(mcs, name, bases, attrs):
        # Register all methods starting with 'api_' as endpoints
        endpoints = {name: method for name, method in attrs.items() 
                    if callable(method) and name.startswith('api_')}
        attrs['_endpoints'] = endpoints
        
        # Add validation for required attributes
        if 'required_attrs' in attrs and not attrs.get('__abstract__', False):
            for attr in attrs['required_attrs']:
                if attr not in attrs:
                    raise TypeError(f"Service {name} missing required attribute: {attr}")
        
        return super().__new__(mcs, name, bases, attrs)

class BaseService(metaclass=ServiceMeta):
    __abstract__ = True
    required_attrs = ['service_name']

class UserService(BaseService):
    service_name = "user_service"
    
    def api_get_user(self, user_id):
        return f"Getting user {user_id}"
    
    def api_create_user(self, user_data):
        return f"Creating user with data {user_data}"
    
    def internal_method(self):
        return "This is internal"

# Usage
service = UserService()
print(f"Service name: {service.service_name}")
print(f"Available endpoints: {list(service._endpoints.keys())}")
print(service.api_get_user(123))

# This would raise TypeError because missing required_attrs
try:
    class BrokenService(BaseService):
        def api_something(self):
            pass
except TypeError as e:
    print(f"Error creating service: {e}")
```

### Dynamic Attribute Access

```python
class DynamicAttributes:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __getattr__(self, name):
        # Called when attribute lookup fails
        return f"Attribute '{name}' not found"

# Usage
obj = DynamicAttributes(x=1, y=2, z="test")
print(obj.x)        # 1
print(obj.y)        # 2
print(obj.z)        # "test"
print(obj.missing)  # "Attribute 'missing' not found"
```

## 3. Concurrency and Parallelism

Python offers several ways to achieve concurrency and parallelism, each with specific use cases.

### Asynchronous Programming with asyncio

```python
import asyncio
import aiohttp
import time

async def fetch_data(url, session):
    print(f"Starting fetch from {url}")
    async with session.get(url) as response:
        data = await response.json()
        print(f"Finished fetch from {url}")
        return data

async def process_urls(urls):
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Create tasks for all URLs and run them concurrently
        tasks = [fetch_data(url, session) for url in urls]
        results = await asyncio.gather(*tasks)
    
    duration = time.time() - start_time
    print(f"Processed {len(urls)} URLs in {duration:.2f} seconds")
    return results

# Example usage
async def main():
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
        "https://jsonplaceholder.typicode.com/posts/4",
        "https://jsonplaceholder.typicode.com/posts/5"
    ]
    
    results = await process_urls(urls)
    return results

# Run the event loop
if __name__ == "__main__":
    results = asyncio.run(main())
    print(f"Fetched {len(results)} results")
```

### Thread-based Concurrency

```python
import threading
import queue
import time
import requests

class Worker(threading.Thread):
    def __init__(self, task_queue, results_queue):
        super().__init__()
        self.task_queue = task_queue
        self.results_queue = results_queue
        self.daemon = True
        
    def run(self):
        while True:
            try:
                # Get a task from the queue
                task_id, url = self.task_queue.get(timeout=3)
                
                # Process the task
                print(f"Thread {self.name} processing {url}")
                response = requests.get(url)
                result = response.status_code, len(response.content)
                
                # Store the result
                self.results_queue.put((task_id, result))
                
                # Mark the task as done
                self.task_queue.task_done()
            except queue.Empty:
                # No more tasks
                break
            except Exception as e:
                print(f"Error in {self.name}: {e}")
                self.task_queue.task_done()

def download_all_sites(sites, num_workers=5):
    # Create queues
    task_queue = queue.Queue()
    results_queue = queue.Queue()
    
    # Enqueue all tasks
    for i, url in enumerate(sites):
        task_queue.put((i, url))
    
    # Create and start worker threads
    workers = []
    for _ in range(num_workers):
        worker = Worker(task_queue, results_queue)
        worker.start()
        workers.append(worker)
    
    # Wait for all tasks to complete
    task_queue.join()
    
    # Get all results
    results = {}
    while not results_queue.empty():
        task_id, result = results_queue.get()
        results[task_id] = result
    
    return results

if __name__ == "__main__":
    sites = [
        "https://www.example.com",
        "https://www.python.org",
        "https://www.github.com",
        "https://www.google.com",
        "https://www.stackoverflow.com"
    ] * 2  # Repeat the list for more tasks
    
    start_time = time.time()
    results = download_all_sites(sites)
    duration = time.time() - start_time
    
    print(f"Downloaded {len(sites)} sites in {duration:.2f} seconds")
    for i, (status, size) in sorted(results.items()):
        print(f"Site {i}: Status {status}, Size {size}")
```

## Interview Questions to Expect

1. "How does Python's memory management work, and how would you diagnose and fix memory leaks?"
2. "Explain the descriptor protocol and give an example of where it's used in Python's standard library."
3. "What is a metaclass, and what problems can it solve in a large Python application?"
4. "When would you use asyncio vs threading vs multiprocessing in Python applications?"
5. "How would you refactor synchronous code to use asynchronous patterns without a complete rewrite?"