import numpy as np
from task import Task
import unittest
##testing

class TestAXIsB(unittest.TestCase):
    def test(self):
        task = Task()
        task.work()
        np.testing.assert_allclose(np.dot(task.a, task.x), task.b, rtol=1e-5, atol=1e-8)


if __name__ == "__main__":
    unittest.main()
