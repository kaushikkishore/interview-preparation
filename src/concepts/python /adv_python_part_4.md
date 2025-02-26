# Advanced Python Concepts for Senior Developers - Part 3

This document covers two advanced Python concepts essential for senior developers with 10+ years of experience: Distributed Systems and Advanced Packaging and Deployment.

## 7. Distributed Systems

Building distributed systems in Python requires handling failures, communication between services, and ensuring consistent state.

### Resilient API Calls with Retries

```python
import time
import random
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests

class ServiceUnavailable(Exception):
    """Custom exception for unavailable service"""
    pass

class InvalidRequestError(Exception):
    """Custom exception for client errors"""
    pass

# Service simulator that sometimes fails
def unreliable_service(failure_rate=0.7):
    """Simulate an unreliable service that sometimes fails"""
    if random.random() < failure_rate:
        if random.random() < 0.5:
            # Simulate a server error (should retry)
            raise ServiceUnavailable("Service temporarily unavailable")
        else:
            # Simulate a client error (should not retry)
            raise InvalidRequestError("Invalid request parameters")
    return {"status": "success", "data": "Some important data"}

# Retry configuration for server errors only
@retry(
    stop=stop_after_attempt(5),                         # Max 5 attempts
    wait=wait_exponential(multiplier=1, min=4, max=10), # Exponential backoff
    retry=retry_if_exception_type(ServiceUnavailable),  # Only retry server errors
    reraise=True                                       # Re-raise last exception
)
def call_with_retry():
    print("Attempting service call...")
    return unreliable_service(failure_rate=0.7)

# Resilient HTTP client
class ResilientHttpClient:
    def __init__(self, base_url, timeout=3, max_retries=3):
        self.base_url = base_url
        self.timeout = timeout
        
        # Create session with retry configuration
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((requests.ConnectionError, 
                                      requests.Timeout, 
                                      requests.HTTPError)),
        reraise=True
    )
    def get(self, endpoint, params=None):
        """Make a GET request with retries for certain error types"""
        url = f"{self.base_url}/{endpoint}"
        try:
            print(f"GET {url}")
            response = self.session.get(
                url, params=params, timeout=self.timeout
            )
            response.raise_for_status()  # Raise exception for 4XX/5XX status codes
            return response.json()
        except requests.HTTPError as e:
            status_code = e.response.status_code
            if status_code >= 500:  # Server errors
                print(f"Server error: {status_code}")
                raise  # Will be retried
            if status_code >= 400:  # Client errors
                print(f"Client error: {status_code}")
                raise  # Won't be retried but propagated
    
    def close(self):
        self.session.close()

# Demonstration
def demonstrate_retry_behavior():
    print("=== Demonstrating retry behavior ===")
    for attempt in range(3):
        try:
            print(f"\nAttempt {attempt + 1}:")
            result = call_with_retry()
            print(f"Success! Result: {result}")
            break
        except ServiceUnavailable:
            print("Service unavailable after maximum retries")
        except InvalidRequestError as e:
            print(f"Client error (not retried): {e}")
            break
```

### Message Queue Processing

```python
import threading
import queue
import time
import random
import uuid

# Message and task definitions
class Message:
    def __init__(self, message_type, payload):
        self.id = str(uuid.uuid4())
        self.type = message_type
        self.payload = payload
        self.created_at = time.time()
    
    def __str__(self):
        return f"Message({self.id}, {self.type}, created {time.time() - self.created_at:.2f}s ago)"

# Worker that processes messages
class Worker(threading.Thread):
    def __init__(self, name, task_queue, result_queue, error_queue=None):
        super().__init__(name=name)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.error_queue = error_queue
        self.daemon = True
        self.running = True
    
    def run(self):
        while self.running:
            try:
                # Get a message with timeout
                message = self.task_queue.get(timeout=1)
                print(f"{self.name} processing {message}")
                
                # Process the message based on type
                if message.type == "calculation":
                    # Simulate calculation
                    time.sleep(random.uniform(0.1, 0.5))
                    result = sum(message.payload)
                    self.result_queue.put((message.id, result))
                
                elif message.type == "transformation":
                    # Simulate data transformation
                    time.sleep(random.uniform(0.2, 0.8))
                    result = [x * 2 for x in message.payload]
                    self.result_queue.put((message.id, result))
                
                else:
                    print(f"{self.name}: Unknown message type: {message.type}")
                    if self.error_queue:
                        self.error_queue.put((message.id, "Unknown message type"))
                
                # Mark task as done
                self.task_queue.task_done()
            
            except queue.Empty:
                # No tasks in the queue
                pass
            except Exception as e:
                print(f"{self.name} error: {e}")
                if self.error_queue:
                    self.error_queue.put((message.id, str(e)))
                self.task_queue.task_done()
    
    def stop(self):
        self.running = False

# Message broker
class MessageBroker:
    def __init__(self, num_workers=3):
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.error_queue = queue.Queue()
        self.workers = []
        
        # Create worker threads
        for i in range(num_workers):
            worker = Worker(
                f"Worker-{i}", 
                self.task_queue, 
                self.result_queue,
                self.error_queue
            )
            self.workers.append(worker)
            worker.start()
    
    def publish(self, message_type, payload):
        """Publish a message to the queue"""
        message = Message(message_type, payload)
        self.task_queue.put(message)
        return message.id
    
    def get_results(self, timeout=None):
        """Get all available results"""
        results = []
        try:
            while True:
                result = self.result_queue.get(block=False)
                results.append(result)
                self.result_queue.task_done()
        except queue.Empty:
            pass
        return results
    
    def get_errors(self):
        """Get all available errors"""
        errors = []
        try:
            while True:
                error = self.error_queue.get(block=False)
                errors.append(error)
                self.error_queue.task_done()
        except queue.Empty:
            pass
        return errors
    
    def wait_for_completion(self):
        """Wait for all tasks to complete"""
        self.task_queue.join()
    
    def shutdown(self):
        """Stop all workers and clean up"""
        for worker in self.workers:
            worker.stop()
        
        for worker in self.workers:
            worker.join(timeout=1)
        
        # Clear the queues
        while not self.task_queue.empty():
            self.task_queue.get()
            self.task_queue.task_done()

# Example usage
def demonstrate_message_queue():
    print("\n=== Demonstrating message queue ===")
    broker = MessageBroker(num_workers=3)
    
    # Publish messages
    message_ids = []
    for i in range(10):
        if i % 2 == 0:
            msg_id = broker.publish("calculation", [i, i+1, i+2])
        else:
            msg_id = broker.publish("transformation", [i, i*i])
        message_ids.append(msg_id)
    
    # Also publish an invalid message type
    broker.publish("invalid_type", ["this will cause an error"])
    
    # Wait for processing to complete
    broker.wait_for_completion()
    
    # Get and print results
    results = broker.get_results()
    print(f"\nResults ({len(results)}):")
    for msg_id, result in results:
        print(f"  Message {msg_id}: {result}")
    
    # Get and print errors
    errors = broker.get_errors()
    print(f"\nErrors ({len(errors)}):")
    for msg_id, error in errors:
        print(f"  Message {msg_id}: {error}")
    
    # Shut down the broker
    broker.shutdown()
```

### Distributed Task Processing with Celery

```python
"""
# This is an example of how to set up Celery for distributed task processing
# Note: This requires external services like RabbitMQ or Redis to run

# tasks.py
from celery import Celery

# Create Celery app
app = Celery('tasks',
             broker='pyamqp://guest@localhost//',  # RabbitMQ
             backend='redis://localhost')          # Redis for results

# Configure Celery
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    worker_concurrency=4,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_time_limit=300,  # 5 minutes
)

# Define a task
@app.task(bind=True, retry_backoff=True, max_retries=3)
def process_data(self, data_id):
    try:
        # Simulating a task that might fail
        print(f"Processing data {data_id}")
        # Load data, process it, save results...
        return {"status": "success", "data_id": data_id}
    except Exception as exc:
        # Log exception and retry the task
        print(f"Task failed: {exc}")
        raise self.retry(exc=exc)

# Chain multiple tasks
@app.task
def preprocess(data_id):
    # Preprocessing logic
    return {"preprocessed_id": data_id}

@app.task
def analyze(preprocessed_data):
    # Analysis logic
    return {"analysis_result": preprocessed_data["preprocessed_id"] * 2}

@app.task
def generate_report(analysis_result):
    # Report generation logic
    return f"Report for result: {analysis_result['analysis_result']}"

# How to use these tasks in application code:
# 
# from tasks import process_data, preprocess, analyze, generate_report
# from celery import chain
#
# # Run a single task
# result = process_data.delay(123)
# print(f"Task ID: {result.id}")
# print(f"Task result: {result.get()}")  # Wait for task to complete
#
# # Run a chain of tasks
# workflow = chain(
#     preprocess.s(42),
#     analyze.s(),
#     generate_report.s()
# )
# result = workflow()
# print(f"Workflow result: {result.get()}")
"""
```

## 8. Advanced Packaging and Deployment

Modern Python applications require standardized packaging, dependency management, and deployment automation.

### Modern Package Structure and pyproject.toml

A modern Python package structure follows conventions that make it easy to distribute, install, and test.

```
# Example of modern project structure
my_package/
  __init__.py
  py.typed         # Type hint marker
  core/
    __init__.py
    models.py
  services/
    __init__.py
    auth.py
  conftest.py      # pytest fixtures
  pyproject.toml   # Modern packaging
```

Example pyproject.toml:

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "build>=0.10.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "1.0.0"
description = "A modern Python package"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
requires-python = ">=3.8"
dependencies = [
    "requests>=2.28.0",
    "sqlalchemy>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=22.0.0",
    "mypy>=0.960",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

Example usage:

```python
from my_package.core.models import User
from my_package.services.auth import authenticate

user = User(id=1, username="test_user")
token = authenticate(user, "password")
```

### Modern Dependency Management with Poetry

Poetry is a modern dependency management and packaging tool that simplifies managing Python projects.

Example poetry.toml:

```toml
[tool.poetry]
name = "advanced-python-app"
version = "0.1.0"
description = "Advanced Python application"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.28.2"
pydantic = "^2.0.0"
sqlalchemy = "^2.0.0"
tenacity = "^8.2.2"

[tool.poetry.group.dev.dependencies]
pytest = "^7.3.1"
black = "^23.3.0"
mypy = "^1.3.0"
flake8 = "^6.0.0"
pytest-cov = "^4.1.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

Example commands for Poetry:

```bash
# Initialize a new project
$ poetry new my-project

# Add dependencies
$ poetry add requests pydantic

# Add dev dependencies
$ poetry add --group dev pytest black

# Install all dependencies
$ poetry install

# Update dependencies
$ poetry update

# Run a command within the virtual environment
$ poetry run python app.py

# Export dependencies to requirements.txt
$ poetry export -f requirements.txt --output requirements.txt
```

### Docker Containerization

Containerizing Python applications ensures consistent deployment across environments.

Example Dockerfile:

```dockerfile
# Example Dockerfile for Python application
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the application
CMD ["python", "app.py"]
```

Docker Compose for multi-container applications:

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/app
    depends_on:
      - db
    volumes:
      - ./:/app
    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

  db:
    image: postgres:14
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=app
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### CI/CD Configuration

Automating testing, building, and deployment is essential for modern development workflows.

Example GitHub Actions workflow:

```yaml
# Example GitHub Actions workflow for Python
name: Python Application CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

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
        pip install poetry
        poetry install
    
    - name: Lint with flake8
      run: |
        poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Type check with mypy
      run: |
        poetry run mypy .
    
    - name: Test with pytest
      run: |
        poetry run pytest --cov=./ --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true

  deploy:
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build and publish
      env:
        TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
        TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
      run: |
        python -m build
        twine upload dist/*
```

## Interview Questions to Expect

1. "How would you design a distributed task processing system in Python?"
2. "Explain how you'd implement retry logic for unreliable API calls in a microservice architecture."
3. "What are the advantages of using containers for Python applications, and how would you structure a multi-container application?"
4. "Walk me through how you would set up a CI/CD pipeline for a Python project."
5. "Compare and contrast different Python packaging approaches and dependency management tools."
6. "How would you implement a message queue in Python, and what are the benefits over direct API calls?"
7. "What strategies would you use to ensure reliability in a distributed Python application?"
8. "Explain how you would structure a Python package for distribution on PyPI and optimal developer experience."

## Conclusion

These advanced concepts around distributed systems and modern packaging/deployment are essential for senior Python developers building scalable, maintainable applications. Understanding these concepts demonstrates the ability to architect complete systems, not just write individual components.