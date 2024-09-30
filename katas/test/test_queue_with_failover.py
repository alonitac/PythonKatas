import unittest
import time
from katas.queue_with_failover import JobQueue


class TestJobQueueL3(unittest.TestCase):

    def test_send_and_get_job(self):
        job_queue = JobQueue(job_timeout=3)

        job_queue.send_job("Job 1")
        job_queue.send_job("Job 2")
        job_queue.send_job("Job 3")

        self.assertEqual(job_queue.size(), 3)

        current_job = job_queue.get_job()
        self.assertIn(current_job, job_queue.hidden_jobs)
        self.assertEqual(job_queue.in_flight_size(), 1)

    def test_job_done(self):
        job_queue = JobQueue(job_timeout=3)

        job_queue.send_job("Job 1")
        current_job = job_queue.get_job()
        job_queue.job_done(current_job)

        self.assertNotIn(current_job, job_queue.hidden_jobs)
        self.assertEqual(job_queue.in_flight_size(), 0)

    def test_return_expired_jobs_to_queue(self):
        job_queue = JobQueue(job_timeout=3)

        job_queue.send_job("Job 1")
        current_job = job_queue.get_job()
        self.assertEqual(job_queue.size(), 0)

        time.sleep(4)
        job_queue.return_expired_jobs_to_queue()

        self.assertNotIn(current_job, job_queue.hidden_jobs)
        self.assertEqual(job_queue.size(), 1)

        with self.assertRaises(ValueError):
            job_queue.job_done(current_job)


if __name__ == '__main__':
    unittest.main()

