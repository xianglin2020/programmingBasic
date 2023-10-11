#! -*- encoding=utf-8 -*-
import time

from Pool import ThreadPool
from Task import Task, AsyncTask


class SimpleTask(Task):
    def __init__(self, _callable):
        super(SimpleTask, self).__init__(_callable)


def process():
    time.sleep(1)
    print('This is a SimpleTask callable function 1.')
    time.sleep(1)
    print('This is a SimpleTask callable function 2.')


def test():
    test_pool = ThreadPool()
    test_pool.start()
    for i in range(10):
        simple_task = SimpleTask(process)
        test_pool.put(simple_task)


def test_async_task():
    def async_process():
        num = 0
        for i in range(100):
            num += i
        return num

    test_pool = ThreadPool()
    test_pool.start()
    for i in range(10):
        async_task = AsyncTask(async_process)
        test_pool.put(async_task)
        result = async_task.get_result()
        print('Get result : %d' % result)


def test_async_task2():
    def async_process(l):
        num = 0
        for i in range(l):
            num += i
        time.sleep(1)
        return num

    test_pool = ThreadPool()
    test_pool.start()

    async_task_list = []
    for i in range(10):
        async_task = AsyncTask(async_process, i)
        test_pool.put(async_task)
        async_task_list.append(async_task)

    for i in range(len(async_task_list)):
        async_task = async_task_list[i]
        print('%d get result in timestamp: %d' % (i, time.time()))
        result = async_task.get_result()
        print('%d get result in timestamp: %d: %d' % (i, time.time(), result))


if __name__ == '__main__':
    test_async_task2()
