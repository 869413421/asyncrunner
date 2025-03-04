import asyncio

from asyncrunner import AsyncWrapper, run_tasks, run_tasks_by_list


async def task(name, duration):
    if duration == 2:
        raise Exception(f"Exception in task '{name}'")
    print(f"任务 '{name}' 开始")
    await asyncio.sleep(duration)
    print(f"任务 '{name}' 完成")
    return [name, duration, f"任务 '{name}' 的结果"]


async def task2(name, duration):
    print(f"task2任务 '{name}' 开始")
    await asyncio.sleep(duration)
    print(f"task2任务 '{name}' 完成")
    return [name, duration, f"task2任务 '{name}' 的结果"]


def coroutine_callback(task):
    task_name = task.get_name() if hasattr(task, "get_name") else task
    print(f"协程回调函数被调用 for task: {task_name}")


async def main():
    info = ["A Task", "B Task", "C Task", "D Task"]

    print("单独添加任务测试:")
    wrapper = AsyncWrapper(concurrency_limit=len(info), timeout=4)
    wrapper.coroutine_callback = coroutine_callback
    for index, item in enumerate(info):
        wrapper.add_coroutine(task, item, index + 1)
    await wrapper.run()

    print("判断执行的任务是否有异常:")
    print(wrapper.has_exception())

    print("任务执行结果:")
    for result in wrapper.get_results():
        if isinstance(result, Exception):
            print(f"Exception: {type(result).__name__} - {result}")
        else:
            print(result)

    task_list = [
        {"target": task, "name": "E Task", "duration": 1},
        {"target": task, "name": "F Task", "duration": 1},
        {"target": task2, "name": "G Task", "duration": 1},
        {"target": task2, "name": "H Task", "duration": 1},
    ]

    results = await run_tasks(task_list, concurrency_limit=4, timeout=2, coroutine_callback=coroutine_callback)
    print("run_tasks 返回结果:")
    for result in results:
        print(result)

    task_params_list = [
        ["I Task", 1],
        ["J Task", 1],
        ["K Task", 1],
    ]

    results = await run_tasks_by_list(task, task_params_list, concurrency_limit=4, timeout=2, coroutine_callback=coroutine_callback)
    print("run_tasks_by_list 返回结果:")
    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
