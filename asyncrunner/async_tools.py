import asyncio
from asyncio import TimeoutError


class TimeoutException(Exception):
    """超时异常"""
    pass


class AsyncWrapper:
    """
    AsyncWrapper 异步 IO 协程封装

    :param concurrency_limit: 同时执行的任务数，None 表示不限制
    :param timeout: 每个任务的超时时间（秒），None 表示不限制
    """

    def __init__(self, concurrency_limit=None, timeout=None):
        self.concurrency_limit = concurrency_limit
        self.timeout = timeout
        self.tasks = []
        self.results = []
        self.coroutine_callback = None
        if concurrency_limit is not None:
            self.semaphore = asyncio.Semaphore(concurrency_limit)
        else:
            self.semaphore = None

    def add_coroutine(self, target, *args, **kwargs):
        async def wrapped_target(*args, **kwargs):
            if self.semaphore:
                async with self.semaphore:
                    return await self._execute(target, *args, **kwargs)
            else:
                return await self._execute(target, *args, **kwargs)

        task = asyncio.create_task(wrapped_target(*args, **kwargs))
        if self.coroutine_callback:
            task.add_done_callback(self.coroutine_callback)
        self.tasks.append(task)
        return task

    async def _execute(self, target, *args, **kwargs):
        try:
            if self.timeout is not None:
                return await asyncio.wait_for(target(*args, **kwargs), timeout=self.timeout)
            else:
                return await target(*args, **kwargs)
        except TimeoutError as e:
            raise TimeoutException(f"Limit Time : {self.timeout} Second") from e
        except Exception as e:
            raise e

    async def run(self):
        """运行所有任务并收集结果"""
        self.results = await asyncio.gather(*self.tasks, return_exceptions=True)

    def has_exception(self):
        """判断是否有任务抛出异常"""
        for task in self.tasks:
            if task.exception() is not None:
                return True
        return False

    def get_results(self):
        return self.results


async def run_tasks(tasks, concurrency_limit=None, coroutine_callback=None, timeout=None):
    """
    根据任务列表运行任务

    Args:
        tasks: 任务列表，每个任务为一个字典，必须包含 key "target" 对应协程函数，其余键值作为参数传入
        concurrency_limit: 同时执行的任务数，None 表示不限制
        coroutine_callback: 任务执行完毕后的回调函数（接收 asyncio.Task 作为参数）
        timeout: 每个任务的超时时间（秒），None 表示不限制

    Returns:
        结果列表，每个结果为任务返回值或异常信息
    """
    wrapper = AsyncWrapper(concurrency_limit=concurrency_limit, timeout=timeout)
    wrapper.coroutine_callback = coroutine_callback

    for task_dict in tasks:
        target = task_dict.pop("target")
        wrapper.add_coroutine(target, **task_dict)

    await wrapper.run()

    results = []
    for result in wrapper.get_results():
        if isinstance(result, Exception):
            results.append(f"Exception: {type(result).__name__} - {result}")
        else:
            results.append(result)
    return results


async def run_tasks_by_list(target: callable, params_list, concurrency_limit=None, coroutine_callback=None, timeout=None):
    """
    根据参数列表运行任务

    Args:
        target: 任务协程函数
        params_list: 参数列表，每个元素可为列表/元组（位置参数）或字典（关键字参数）
        concurrency_limit: 同时执行的任务数，None 表示不限制
        coroutine_callback: 任务执行完毕后的回调函数
        timeout: 每个任务的超时时间（秒），None 表示不限制

    Returns:
        结果列表，每个结果为任务返回值或异常信息
    """
    wrapper = AsyncWrapper(concurrency_limit=concurrency_limit, timeout=timeout)
    wrapper.coroutine_callback = coroutine_callback

    for params in params_list:
        if isinstance(params, (list, tuple)):
            wrapper.add_coroutine(target, *params)
        elif isinstance(params, dict):
            wrapper.add_coroutine(target, **params)
        else:
            # 单个参数情况
            wrapper.add_coroutine(target, params)

    await wrapper.run()

    results = []
    for result in wrapper.get_results():
        if isinstance(result, Exception):
            results.append(f"Exception: {type(result).__name__} - {result}")
        else:
            results.append(result)
    return results
