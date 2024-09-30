import unittest
from datetime import datetime
from katas.tasks_scheduling import tasks_scheduling

ISO_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class TestTaskSchedulingL4(unittest.TestCase):

    def test_task_scheduling(self):
        tasks = [
            (datetime.strptime('2022-01-01T13:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:00:00Z', ISO_FORMAT)),
            (datetime.strptime('2022-01-01T13:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:30:00Z', ISO_FORMAT)),
            (datetime.strptime('2022-01-01T11:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T16:00:00Z', ISO_FORMAT)),
            (datetime.strptime('2022-01-01T14:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:05:00Z', ISO_FORMAT)),
            (datetime.strptime('2022-01-01T12:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T13:30:00Z', ISO_FORMAT)),
            (datetime.strptime('2022-01-01T10:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T10:10:00Z', ISO_FORMAT))
        ]

        result = tasks_scheduling(tasks)
        self.assertEqual(result, [5, 4, 3])


if __name__ == '__main__':
    unittest.main()
