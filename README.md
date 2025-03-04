# asyncrunner

[English](README.md) | [中文](README_zh.md)

**asyncrunner** is an asyncio-based asynchronous task runner designed to help you easily implement concurrent task management. It supports task timeout control, concurrency limits, and callback functions after task completion, meeting most asynchronous task scheduling needs.

## Installation

You can install the package via pip:

```bash
pip install async-task-runner
```

Or build and install using [Poetry](https://python-poetry.org/):

```bash
# Build package (in project root directory)
poetry build

# Install the generated package (assuming the generated file is async-task-runner-1.0.0-py3-none-any.whl)
pip install dist/async-task-runner-1.0.0-py3-none-any.whl
```

## Features

- **High-performance Async Scheduling**: Implemented based on asyncio, fully utilizing Python's asynchronous features
- **Concurrency Control**: Uses `asyncio.Semaphore` to control the number of simultaneously running tasks
- **Task Timeout Control**: Uses `asyncio.wait_for` to set timeout for each task
- **Task Callbacks**: Supports triggering callback functions after task completion
- **Flexible Task Scheduling Interface**:
    - `run_tasks`: Schedule tasks through a list of task dictionaries, each task dictionary should contain `target` (task coroutine function) and other parameters
    - `run_tasks_by_list`: Schedule tasks through parameter lists, suitable for cases where parameters are provided in list/tuple or dictionary form

## Usage

```python
import asyncio
from asyncrunner import AsyncRunner

async def example_task(x):
    await asyncio.sleep(1)
    return x * 2

async def main():
    # Create runner instance
    runner = AsyncRunner(max_workers=3)  # Limit concurrent tasks to 3
    
    # Prepare tasks
    tasks = [
        {"target": example_task, "args": (i,)} for i in range(5)
    ]
    
    # Run tasks and get results
    results = await runner.run_tasks(tasks)
    print(results)  # [0, 2, 4, 6, 8]

if __name__ == "__main__":
    asyncio.run(main())
```

## License

This project is licensed under the MIT License.
