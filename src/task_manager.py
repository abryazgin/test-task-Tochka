from queue import Queue
from threading import Thread


class TaskManager:
    """
    Менеджер задач
    """
    def __init__(self, worker_count):
        self.tasks = Queue()
        self.threads = []
        for _ in range(worker_count):
            thread = Thread(target=worker, args=(self, ))
            thread.start()
            self.threads.append(thread)

    def finish(self):
        for _ in self.threads:
            self.add(None)
        self.tasks.join()

    def get(self):
        return self.tasks.get()

    def add(self, task, args=None, kwargs=None):
        self.tasks.put((task, args or tuple(), kwargs or dict(), ))

    def task_done(self):
        self.tasks.task_done()


def worker(tm):
    while True:
        task, args, kwargs = tm.get()
        try:
            if task is None:
                break
            task(*args, **kwargs)
        finally:
            tm.task_done()


if __name__ == '__main__':
    def task(n):
        print('task {i} started'.format(i=n))
        import time
        time.sleep(1)
        print('task {i} ended'.format(i=n))

    tm = TaskManager(5)
    print('Task creation started')
    for i in range(10):
        tm.add(task, args=(i, ))
    print('Task creation ended')
    tm.finish()
    print('Tasks done')
