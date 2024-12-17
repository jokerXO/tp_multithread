from multiprocessing import Queue
from multiprocessing.managers import BaseManager


# Création des queues partagées
task_queue = Queue()
result_queue = Queue()

# Création d'une classe pour exposer les queues
class QueueManager(BaseManager):
    pass
class QueueClient():
    def __init__(self, host, port, authkey):
        self.host = host
        self.port = port
        self.authkey = authkey
        
    def start_server(self, task_queue, result_queue):
        QueueManager.register('get_task_queue', callable=lambda: task_queue)
        QueueManager.register('get_result_queue', callable=lambda: result_queue)

        manager = QueueManager(address=(self.host, self.port), authkey=self.authkey)
        server = manager.get_server()
        print(f"Server started on {self.host}:{self.port}")
        server.serve_forever()

    def connect_to_server(self):
        QueueManager.register('get_task_queue')
        QueueManager.register('get_result_queue')
        manager = QueueManager(address=(self.host, self.port), authkey=self.authkey)
        manager.connect()
        self.task_queue = manager.get_task_queue()
        self.result_queue = manager.get_result_queue()
        print(f"Connected to server on {self.host}:{self.port}")




if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 5000
    AUTHKEY = b'abc'

    task_queue = Queue()
    result_queue = Queue()
    server = QueueClient(HOST, PORT, AUTHKEY)
    server.start_server(task_queue, result_queue)