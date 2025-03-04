# asyncrunner

[English](README.md) | [中文](README_zh.md)

**asyncrunner** 是一个基于 asyncio 的异步任务运行器，旨在帮助你轻松实现并发任务管理。它支持任务超时控制、并发限制以及任务完成后的回调函数，能够满足大部分异步任务调度的需求。

## 特性

- **高性能异步调度**：基于 asyncio 实现，充分利用 Python 异步特性
- **并发限制**：使用 `asyncio.Semaphore` 控制同时运行的任务数
- **任务超时控制**：使用 `asyncio.wait_for` 为每个任务设置超时
- **任务回调**：支持在任务完成后触发回调函数
- **灵活的任务调度接口**：
    - `run_tasks`：通过任务字典列表调度任务，每个任务字典需要包含 `target`（任务协程函数）以及其他参数
    - `run_tasks_by_list`：通过参数列表调度任务，适用于参数以列表/元组或字典形式提供的情况

## 安装

使用 [Poetry](https://python-poetry.org/) 构建并安装：

```bash
# 构建安装包（在项目根目录下）
poetry build

# 安装生成的包（假设生成的文件名为 asyncrunner-1.0.0-py3-none-any.whl）
pip install dist/asyncrunner-1.0.0-py3-none-any.whl
```

## 使用示例

```python
import asyncio
from asyncrunner import AsyncRunner

async def example_task(x):
    await asyncio.sleep(1)
    return x * 2

async def main():
    # 创建运行器实例
    runner = AsyncRunner(max_workers=3)  # 限制并发任务数为3
    
    # 准备任务
    tasks = [
        {"target": example_task, "args": (i,)} for i in range(5)
    ]
    
    # 运行任务并获取结果
    results = await runner.run_tasks(tasks)
    print(results)  # [0, 2, 4, 6, 8]

if __name__ == "__main__":
    asyncio.run(main())
```

## 许可证

本项目采用 MIT 许可证。 