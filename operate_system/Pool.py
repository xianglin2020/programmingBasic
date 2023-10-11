#! -*- encoding=utf-8 -*-
import threading
import psutil
from Task import Task, AsyncTask
from Queue import ThreadSafeQueue


# 任务处理线程
class ProcessThread(threading.Thread):
    def __init__(self, task_queue, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.task_queue = task_queue
        self.args = args
        self.kwargs = kwargs
        # 任务线程停止标记
        self.dismiss_flag = threading.Event()

    pass

    def run(self):
        while True:
            # 判断线程是否被要求停止
            if self.dismiss_flag.is_set():
                break
            task = self.task_queue.pop()
            if not isinstance(task, Task):
                continue
            # 执行 task 实际逻辑
            result = task.callable(*task.args, **task.kwargs)
            if isinstance(task, AsyncTask):
                task.set_result(result)

    def _dismiss(self):
        self.dismiss_flag.set()

    def stop(self):
        self._dismiss()
        pass


# 线程池
class ThreadPool:
    def __init__(self, size=0):
        if not size:
            size = psutil.cpu_count() * 2
        self.pool = ThreadSafeQueue(size)
        self.task_queue = ThreadSafeQueue()
        for i in range(size):
            self.pool.put(ProcessThread(self.task_queue))

    def start(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.start()

    # 停止线程池
    def join(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.stop()
        while self.pool.size():
            thread = self.pool.pop()
            thread.join()

    # 往线程池提交任务
    def put(self, item):
        if not isinstance(item, Task):
            raise TaskTypeErrorException()
        self.task_queue.put(item)

    def batch_put(self, item_list):
        if not isinstance(item_list, list):
            item_list = list(item_list)
        for item in item_list:
            self.put(item)

    def size(self):
        return self.pool.size()


class TaskTypeErrorException(Exception):
    pass
