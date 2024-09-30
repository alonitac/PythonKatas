import unittest
from katas.nginx_log_parser import nginx_logs_parser


class TestNginxLogsParserL2(unittest.TestCase):

    def test_nginx_logs_parser(self):
        logs = [
            '46.113.254.56 - - [05/Feb/2024:08:29:40 +0000] "GET /adapter/global/Cross-group-support.png HTTP/1.1" 200 1167 "-" "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/5310 (KHTML, like Gecko) Chrome/40.0.895.0 Mobile Safari/5310"',
            '26.135.132.29 - - [05/Feb/2024:08:29:45 +0000] "GET /zero%20administration/Cross-group/process%20improvement.hmtl HTTP/1.1" 200 820 "-" "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_1 rv:4.0; en-US) AppleWebKit/533.18.8 (KHTML, like Gecko) Version/4.2 Safari/533.18.8"',
            '169.209.142.178 - - [05/Feb/2024:08:29:45 +0000] "GET /Cloned-needs-based.htm HTTP/1.1" 200 2906 "-" "Mozilla/5.0 (Windows 95) AppleWebKit/5341 (KHTML, like Gecko) Chrome/36.0.842.0 Mobile Safari/5341"',
        ]

        expected_results = [
            {
                'client_ip': '46.113.254.56',
                'date': '05/Feb/2024:08:29:40 +0000',
                'http_method': 'GET',
                'path': '/adapter/global/Cross-group-support.png',
                'http_version': '1.1',
                'status': 200,
                'response_bytes': 1167,
                'user_agent': 'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/5310 (KHTML, like Gecko) Chrome/40.0.895.0 Mobile Safari/5310'
            },
            {
                'client_ip': '26.135.132.29',
                'date': '05/Feb/2024:08:29:45 +0000',
                'http_method': 'GET',
                'path': '/zero%20administration/Cross-group/process%20improvement.hmtl',
                'http_version': '1.1',
                'status': 200,
                'response_bytes': 820,
                'user_agent': 'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_1 rv:4.0; en-US) AppleWebKit/533.18.8 (KHTML, like Gecko) Version/4.2 Safari/533.18.8'
            },
            {
                'client_ip': '169.209.142.178',
                'date': '05/Feb/2024:08:29:45 +0000',
                'http_method': 'GET',
                'path': '/Cloned-needs-based.htm',
                'http_version': '1.1',
                'status': 200,
                'response_bytes': 2906,
                'user_agent': 'Mozilla/5.0 (Windows 95) AppleWebKit/5341 (KHTML, like Gecko) Chrome/36.0.842.0 Mobile Safari/5341'
            },
        ]

        for log, expected_result in zip(logs, expected_results):
            result = nginx_logs_parser(log)
            self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
