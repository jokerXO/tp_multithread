from multiprocessing import Queue
from multiprocessing.managers import BaseManager


# Création des queues partagées
task_queue = Queue()
result_queue = Queue()


# Création d'une classe pour exposer les queues
class QueueManager(BaseManager):
    pass


if __name__ == "__main__":
    QueueManager.register("get_task_queue", callable=lambda: task_queue)
    QueueManager.register("get_result_queue", callable=lambda: result_queue)

    manager = QueueManager(address=("127.0.0.1", 50000), authkey=b"abc")
    print("Démarrage du serveur...")
    server = manager.get_server()
    print("server lancé !")
    server.serve_forever()
