from multiprocessing.managers import BaseManager
import time


class QueueClient(BaseManager):
    pass


if __name__ == "__main__":
    # Enregistrement des queues côté client
    QueueClient.register("get_task_queue")
    QueueClient.register("get_result_queue")

    # Connexion au serveur
    client = QueueClient(address=("127.0.0.1", 50000), authkey=b"abc")
    client.connect()

    # Récupérer les queues
    task_queue = client.get_task_queue()
    result_queue = client.get_result_queue()

    print("Minion: En attente de tâches...")
    while True:
        if not task_queue.empty():
            task = task_queue.get()
            print(f"Minion: Traitement de {task}")
            time.sleep(2)  # Simuler un traitement
            task.work()
            result_queue.put(task)
            print("Minion: tache traitee !")
        else:
            print("Minion: Attente...")
            time.sleep(1)
