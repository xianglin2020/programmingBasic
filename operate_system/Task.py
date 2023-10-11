#! -*- encoding=utf-8 -*-
import threading
import uuid


# 基本任务对象
class Task:
    def __init__(self, func, *args, **kwargs):
        self.id = uuid.uuid4()
        self.callable = func
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return 'Task id: ' + str(self.id)


# 异步任务对象
class AsyncTask(Task):
    def __init__(self, func, *args, **kwargs):
        self.result = None
        self.condition = threading.Condition()
        super().__init__(func, *args, **kwargs)

    # 设置运行结果
    def set_result(self, result):
        self.condition.acquire()
        self.result = result
        self.condition.notify()
        self.condition.release()

    # 获取认为结果
    def get_result(self):
        self.condition.acquire()
        if not self.result:
            self.condition.wait()
        result = self.result
        self.condition.release()
        return result


def my_function():
    print('this is a task test.')


if __name__ == '__main__':
    task = Task(func=my_function)
    print(task)
