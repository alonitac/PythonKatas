import unittest
from unittest.mock import patch
from katas.ansible_dynamic_inv import ansible_dynamic_inv
import re


def parse_ansible_inventory(output):
    pattern = re.compile(r'\[([^\]]+)\]\n((?:.*\d+\.\d+\.\d+\.\d+.*\n)+)')
    matches = pattern.findall(output)
    parsed_data = {}

    for match in matches:
        group_name, ip_addresses = match
        parsed_data[group_name] = ip_addresses.strip().split('\n')

    return parsed_data


class TestAnsibleDynamicInvL3(unittest.TestCase):
    @patch('requests.get')
    def test_ansible_dynamic_inv(self, mock_requests_get):
        mock_response = {
            "verifiable_password_authentication": False,
            "ssh_key_fingerprints": {
                "SHA256_ECDSA": "p2QAMXNIC1TJYWeIOttrVc98/R1BUFWu3/LiyKgUfQM",
                "SHA256_ED25519": "+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU",
                "SHA256_RSA": "uNiVztksCsDhcc0u9e8BujQXVUpKZIDTMczCvj3tD2s"
            },
            "ssh_keys": [
                "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl",
                "ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBEmKSENjQEezOmxkZMy7opKgwFB9nkt5YRrYMjNuG5N87uRgg6CLrbo5wAdT/y6v0mKV0U2w0WZ2YB/++Tpockg=",
                "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCj7ndNxQowgcQnjshcLrqPEiiphnt+VTTvDP6mHBL9j1aNUkY4Ue1gvwnGLVlOhGeYrnZaMgRK6+PKCUXaDbC7qtbW8gIkhL7aGCsOr/C56SJMy/BCZfxd1nWzAOxSDPgVsmerOBYfNqltV9/hWCqBywINIR+5dIg6JTJ72pcEpEjcYgXkE2YEFXV1JHnsKgbLWNlhScqb2UmyRkQyytRLtL+38TGxkxCflmO+5Z8CSSNY7GidjMIZ7Q4zMjA2n1nGrlTDkzwDCsw+wqFPGQA179cnfGWOWRVruj16z6XyvxvjJwbz0wQZ75XK5tKSb7FNyeIEs4TT4jk+S4dhPeAUC5y+bDYirYgM4GC7uEnztnZyaVWQ7B381AK4Qdrwt51ZqExKbQpTUNn+EjqoTwvqNj4kqx5QUCI0ThS/YkOxJCXmPUWZbhjpCg56i+2aB6CmK2JGhn57K5mj0MNdBXA4/WnwH6XoPWJzK5Nyu2zB3nAZp+S5hpQs+p1vN1/wsjk="
            ],
            "hooks": ["192.30.252.0/22"],
            "web": ["192.30.252.0/22", "2606:50c0::/32", "20.201.28.151/32"],
            "api": ["192.30.252.0/22", "2606:50c0::/32", "20.201.28.148/32"],
            "git": ["192.30.252.0/22", "2606:50c0::/32", "20.201.28.151/32"],
            "github_enterprise_importer": ["192.30.252.0/22"],
            "packages": ["140.82.121.33/32"],
            "pages": ["192.30.252.153/32", "192.30.252.154/32"],
            "importer": ["52.23.85.212/32"],
            "actions": ["52.22.155.48/32"],
            "dependabot": ["18.213.123.130/32"],
            "domains": {
                "website": ["*.github.com"],
                "codespaces": ["*.github.com"],
                "copilot": ["*.github.com"],
                "packages": ["*.github.com"],
                "actions": ["productionresultssa0.blob.core.windows.net"]
            }
        }
        mock_requests_get.return_value.json.return_value = mock_response
        ansible_dynamic_inv()

        with open('hosts') as f:
            inv = f.read()

        try:
            inv_parsed = parse_ansible_inventory(inv)
        except:
            raise RuntimeError("""Failed to parse inventory. The expected inv form is: 
[group_name]
some text followed by ip 0.0.0.0 some text again

[web]
192.168.1.1
192.168.1.2
            """)

        for group in ['web', 'api', 'git']:
            self.assertIn(group, inv_parsed)

            for expected_ip in mock_response[group]:
                if expected_ip.endswith('/32') and ':' not in expected_ip:
                    self.assertIn(expected_ip[:-3], ' '.join(inv_parsed[group]))


if __name__ == '__main__':
    unittest.main()
