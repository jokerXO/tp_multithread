import time
import json
import numpy as np




class Task:
    def __init__(self, identifier=0, size=None):
        self.identifier = identifier
        # choosee the size of the problem
        self.size = size or np.random.randint(300, 3_000)
        # Generate the input of the problem
        self.a = np.random.rand(self.size, self.size)
        self.b = np.random.rand(self.size)
        # prepare room for the results
        self.x = np.zeros((self.size))
        self.time = 0

    def work(self):
        start = time.perf_counter()
        self.x = np.linalg.solve(self.a, self.b)
        self.time = time.perf_counter() - start

    def __str__(self):
        return f"tache {self.identifier}"
    
    def to_json(self) -> str:
        info = {"identifier":self.identifier,"size":self.size,"a":self.a.tolist(),"b":self.b.tolist(),"x":self.x.tolist(),"time":self.time}
        return json.dumps(info)
        
    @staticmethod
    def from_json(text: str) -> "Task":
        data = json.loads(text)
        task = Task(identifier=data.get("identifier", 0), size=data.get("size"))
        task.time = data.get("time", 0)
        task.x = np.array(data.get("x", np.zeros((task.size,))))
        task.a = np.array(data.get("a", np.random.rand(task.size, task.size)))
        task.b = np.array(data.get("b", np.random.rand(task.size)))
        
        return task

    def __eq__(self, other: "Task") -> bool:
        if type(other) != type(self):
            return False
        return (np.array_equal(self.a, other.a) and np.array_equal(self.x, other.x)  and np.array_equal(self.b, other.b)  and self.time == other.time and self.identifier == other.identifier)
                
 
 


if __name__ == "__main__" :
     task =  Task(identifier=1)
     text = task.to_json()
     task.from_json(text)
     
    