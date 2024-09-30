import json
import unittest
from katas.json_configs_merge import json_configs_merge


class TestJsonConfigsMergeL2(unittest.TestCase):

    def test_json_configs_merge(self):
        default_json_path = 'configs/default.json'
        local_json_path = 'configs/local.json'
        result = json_configs_merge(default_json_path, local_json_path)

        expected_result = {
            "in_cluster": False,
            "cloud_client": "gcloud",
            "data-collector": {
                "filename_datetime_fmt": "%Y-%m-%dT%H-%M-%SZ",
                "batch_duration_sec": 3600,
                "batch_safety_margin_before_close_sec": 600,
                "kafka": {
                    "local": True,
                    "consumers_group": "data-collector-3-local",
                    "data_topics": ["^.*_data$"]
                }
            },
            "job-scheduler": {
                "jobs_collection": "scheduler_jobs_local",
                "kafka": {
                    "jobs_status_topic": "jobs-status-topic",
                    "consumers_group": "job-scheduler"
                }
            },
            "data": {
                "local_data_path": "/var/lib/data",
                "uploader_dir": "uploader-data",
                "collector_dir": "collector-data"
            },
            "kafka": {
                "bootstrap_server": "localhost:9092"
            },
            "mongodb": {
                "host": "mongodb-svc",
                "port": 27017
            },
            "elasticsearch": {
                "host": "http://elasticsearch-svc:9200"
            },
            "grafana": {
                "host": "grafana-svc:3000"
            },
            "fluentbit": {
                "input_host": "fluent-bit-svc:8888"
            },
            "git-server": {
                "host": "http://git-svc.default.svc.cluster.local:8083"
            }
        }

        expected_result_json = json.dumps(expected_result, sort_keys=True)
        result_json = json.dumps(result, sort_keys=True)
        self.assertEqual(result_json, expected_result_json)


if __name__ == '__main__':
    unittest.main()
