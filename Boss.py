from multiprocessing.managers import BaseManager
from task import Task


class QueueClient(BaseManager):
    pass


if __name__ == "__main__":
    QueueClient.register("get_task_queue")
    QueueClient.register("get_result_queue")

    client = QueueClient(address=("127.0.0.1", 50000), authkey=b"abc")
    client.connect()

    task_queue = client.get_task_queue()
    result_queue = client.get_result_queue()

    print("Boss: Ajout de tâches")
    for i in range(10):
        task = Task(identifier=i)
        task_queue.put(task)
        print(f"Boss: Tâche ajoutée - {task}")
