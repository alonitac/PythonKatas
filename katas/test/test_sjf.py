import unittest
from katas.sjf import is_empty, push, pop


class TestJobQueueL2(unittest.TestCase):

    def test_push_and_is_empty(self):
        jobs_queue = []
        self.assertTrue(is_empty(jobs_queue))

        push(jobs_queue, "Job1", 5)
        self.assertFalse(is_empty(jobs_queue))

    def test_pop_highest_throughput(self):
        jobs_queue = [("Job1", 5), ("Job2", 8), ("Job3", 2), ("Job4", 10)]

        result = pop(jobs_queue)
        self.assertEqual(result, ("Job3", 2))

        result = pop(jobs_queue)
        self.assertEqual(result, ("Job1", 5))

        result = pop(jobs_queue)
        self.assertEqual(result, ("Job2", 8))


if __name__ == '__main__':
    unittest.main()
