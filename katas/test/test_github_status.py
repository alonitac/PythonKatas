import unittest
from unittest.mock import patch, MagicMock
from katas.github_status import github_status


def side_effect_bad(url, *args, **kwargs):
    if 'v2/summary.json' in url:
        res = {
            "page": {
                "id": "kctbh9vrtdwd",
                "name": "GitHub",
                "url": "https://www.githubstatus.com",
                "updated_at": "2024-02-05T08:31:08Z"
            },
            "status": {
                "description": "Partial System Outage",
                "indicator": "major"
            },
            "components": [
                {
                    "created_at": "2014-05-03T01:22:07.274Z",
                    "description": None,
                    "id": "b13yz5g2cw10",
                    "name": "API",
                    "page_id": "kctbh9vrtdwd",
                    "position": 1,
                    "status": "partial_outage",
                    "updated_at": "2014-05-14T20:34:43.340Z"
                },
                {
                    "created_at": "2014-05-03T01:22:07.286Z",
                    "description": None,
                    "id": "9397cnvk62zn",
                    "name": "Management Portal",
                    "page_id": "kctbh9vrtdwd",
                    "position": 2,
                    "status": "major_outage",
                    "updated_at": "2014-05-14T20:34:44.470Z"
                }
            ],
            "incidents": [
                {
                    "created_at": "2014-05-14T14:22:39.441-06:00",
                    "id": "cp306tmzcl0y",
                    "impact": "critical",
                    "incident_updates": [
                        {
                            "body": "Our master database has ham sandwiches flying out of the rack, and we're working our hardest to stop the bleeding. The whole site is down while we restore functionality, and we'll provide another update within 30 minutes.",
                            "created_at": "2014-05-14T14:22:40.301-06:00",
                            "display_at": "2014-05-14T14:22:40.301-06:00",
                            "id": "jdy3tw5mt5r5",
                            "incident_id": "cp306tmzcl0y",
                            "status": "identified",
                            "updated_at": "2014-05-14T14:22:40.301-06:00"
                        }
                    ],
                    "monitoring_at": None,
                    "name": "Unplanned Database Outage",
                    "page_id": "kctbh9vrtdwd",
                    "resolved_at": None,
                    "shortlink": "http://stspg.co:5000/Q0E",
                    "status": "identified",
                    "updated_at": "2014-05-14T14:35:21.711-06:00"
                }
            ],
            "scheduled_maintenances": [
                {
                    "created_at": "2014-05-14T14:24:40.430-06:00",
                    "id": "w1zdr745wmfy",
                    "impact": "none",
                    "incident_updates": [
                        {
                            "body": "Our data center has informed us that they will be performing routine network maintenance. No interruption in service is expected. Any issues during this maintenance should be directed to our support center",
                            "created_at": "2014-05-14T14:24:41.913-06:00",
                            "display_at": "2014-05-14T14:24:41.913-06:00",
                            "id": "qq0vx910b3qj",
                            "incident_id": "w1zdr745wmfy",
                            "status": "scheduled",
                            "updated_at": "2014-05-14T14:24:41.913-06:00"
                        }
                    ],
                    "monitoring_at": None,
                    "name": "Network Maintenance (No Interruption Expected)",
                    "page_id": "kctbh9vrtdwd",
                    "resolved_at": None,
                    "scheduled_for": "2014-05-17T22:00:00.000-06:00",
                    "scheduled_until": "2014-05-17T23:30:00.000-06:00",
                    "shortlink": "http://stspg.co:5000/Q0F",
                    "status": "scheduled",
                    "updated_at": "2014-05-14T14:24:41.918-06:00"
                },
                {
                    "created_at": "2014-05-14T14:27:17.303-06:00",
                    "id": "k7mf5z1gz05c",
                    "impact": "minor",
                    "incident_updates": [
                        {
                            "body": "Scheduled maintenance is currently in progress. We will provide updates as necessary.",
                            "created_at": "2014-05-14T14:34:20.036-06:00",
                            "display_at": "2014-05-14T14:34:20.036-06:00",
                            "id": "drs62w8df6fs",
                            "incident_id": "k7mf5z1gz05c",
                            "status": "in_progress",
                            "updated_at": "2014-05-14T14:34:20.036-06:00"
                        },
                        {
                            "body": "We will be performing rolling upgrades to our web tier with a new kernel version so that Heartbleed will stop making us lose sleep at night. Increased load and latency is expected, but the app should still function appropriately. We will provide updates every 30 minutes with progress of the reboots.",
                            "created_at": "2014-05-14T14:27:18.845-06:00",
                            "display_at": "2014-05-14T14:27:18.845-06:00",
                            "id": "z40y7398jqxc",
                            "incident_id": "k7mf5z1gz05c",
                            "status": "scheduled",
                            "updated_at": "2014-05-14T14:27:18.845-06:00"
                        }
                    ],
                    "monitoring_at": None,
                    "name": "Web Tier Recycle",
                    "page_id": "kctbh9vrtdwd",
                    "resolved_at": None,
                    "scheduled_for": "2014-05-14T14:30:00.000-06:00",
                    "scheduled_until": "2014-05-14T16:30:00.000-06:00",
                    "shortlink": "http://stspg.co:5000/Q0G",
                    "status": "in_progress",
                    "updated_at": "2014-05-14T14:35:12.258-06:00"
                }
            ]
        }
    elif 'v2/components.json' in url:
        res = {
            "page": {
                "id": "kctbh9vrtdwd",
                "name": "GitHub",
                "url": "https://www.githubstatus.com",
                "updated_at": "2024-02-05T08:31:08Z"
            },
            "components": [
                {
                    "created_at": "2014-05-03T01:22:07.274Z",
                    "description": None,
                    "group": False,
                    "group_id": None,
                    "id": "b13yz5g2cw10",
                    "name": "API",
                    "only_show_if_degraded": False,
                    "page_id": "kctbh9vrtdwd",
                    "position": 1,
                    "showcase": True,
                    "start_date": None,
                    "status": "partial_outage",
                    "updated_at": "2014-05-14T20:34:43.340Z"
                },
                {
                    "created_at": "2014-05-03T01:22:07.286Z",
                    "description": None,
                    "group": False,
                    "group_id": None,
                    "id": "9397cnvk62zn",
                    "name": "Management Portal",
                    "only_show_if_degraded": False,
                    "page_id": "kctbh9vrtdwd",
                    "position": 2,
                    "showcase": True,
                    "start_date": None,
                    "status": "major_outage",
                    "updated_at": "2014-05-14T20:34:44.470Z"
                }
            ]
        }
    elif 'v2/status.json' in url:
        res = {
            "page": {
                "id": "kctbh9vrtdwd",
                "name": "GitHub",
                "url": "https://www.githubstatus.com",
                "updated_at": "2024-02-05T08:31:08Z"
            },
            "status": {
                "description": "Partial System Outage",
                "indicator": "major"
            }
        }
    else:
        res = {}

    mock_object = MagicMock()
    mock_object.json.return_value = res
    mock_object.content.return_value = str(res).encode('utf-8')
    mock_object.text.return_value = str(res)
    mock_object.status_code = 200
    return mock_object


def side_effect_good(url, *args, **kwargs):
    if 'v2/summary.json' in url:
        res = {
            "page": {
                "id": "kctbh9vrtdwd",
                "name": "GitHub",
                "url": "https://www.githubstatus.com",
                "time_zone": "Etc/UTC",
                "updated_at": "2024-02-05T08:31:08.006Z"
            },
            "components": [
                {
                    "id": "8l4ygp009s5s",
                    "name": "Git Operations",
                    "status": "operational",
                    "created_at": "2017-01-31T20:05:05.370Z",
                    "updated_at": "2024-01-09T14:32:53.456Z",
                    "position": 1,
                    "description": "Performance of git clones, pulls, pushes, and associated operations",
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "brv1bkgrwx7q",
                    "name": "API Requests",
                    "status": "operational",
                    "created_at": "2017-01-31T20:01:46.621Z",
                    "updated_at": "2024-01-09T14:24:13.860Z",
                    "position": 2,
                    "description": "Requests for GitHub APIs",
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "4230lsnqdsld",
                    "name": "Webhooks",
                    "status": "operational",
                    "created_at": "2019-11-13T18:00:24.256Z",
                    "updated_at": "2024-01-09T14:20:01.432Z",
                    "position": 3,
                    "description": "Real time HTTP callbacks of user-generated and system events",
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "0l2p9nhqnxpd",
                    "name": "Visit www.githubstatus.com for more information",
                    "status": "operational",
                    "created_at": "2018-12-05T19:39:40.838Z",
                    "updated_at": "2022-09-07T00:08:33.519Z",
                    "position": 4,
                    "description": None,
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "kr09ddfgbfsf",
                    "name": "Issues",
                    "status": "operational",
                    "created_at": "2017-01-31T20:01:46.638Z",
                    "updated_at": "2024-01-09T14:24:02.127Z",
                    "position": 5,
                    "description": "Requests for Issues on GitHub.com",
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "hhtssxt0f5v2",
                    "name": "Pull Requests",
                    "status": "operational",
                    "created_at": "2020-09-02T15:39:06.329Z",
                    "updated_at": "2024-01-09T14:38:57.170Z",
                    "position": 6,
                    "description": "Requests for Pull Requests on GitHub.com",
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "br0l2tvcx85d",
                    "name": "Actions",
                    "status": "operational",
                    "created_at": "2019-11-13T18:02:19.432Z",
                    "updated_at": "2024-01-21T06:19:52.242Z",
                    "position": 7,
                    "description": "Workflows, Compute and Orchestration for GitHub Actions",
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "st3j38cctv9l",
                    "name": "Packages",
                    "status": "operational",
                    "created_at": "2019-11-13T18:02:40.064Z",
                    "updated_at": "2024-01-09T14:37:18.000Z",
                    "position": 8,
                    "description": "API requests and webhook delivery for GitHub Packages",
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "vg70hn9s2tyj",
                    "name": "Pages",
                    "status": "operational",
                    "created_at": "2017-01-31T20:04:33.923Z",
                    "updated_at": "2024-01-09T14:16:28.324Z",
                    "position": 9,
                    "description": "Frontend application and API servers for Pages builds",
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "h2ftsgbw7kmk",
                    "name": "Codespaces",
                    "status": "operational",
                    "created_at": "2021-08-11T16:02:09.505Z",
                    "updated_at": "2024-01-21T09:34:34.651Z",
                    "position": 10,
                    "description": "Orchestration and Compute for GitHub Codespaces",
                    "showcase": False,
                    "start_date": "2021-08-11",
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "pjmpxvq2cmr2",
                    "name": "Copilot",
                    "status": "operational",
                    "created_at": "2022-06-21T16:04:33.017Z",
                    "updated_at": "2023-12-01T18:16:24.775Z",
                    "position": 11,
                    "description": None,
                    "showcase": False,
                    "start_date": "2022-06-21",
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                }
            ],
            "incidents": [],
            "scheduled_maintenances": [],
            "status": {
                "indicator": "none",
                "description": "All Systems Operational"
            }
        }
    elif 'v2/components.json' in url:
        res = {
            "page": {
                "id": "kctbh9vrtdwd",
                "name": "GitHub",
                "url": "https://www.githubstatus.com",
                "time_zone": "Etc/UTC",
                "updated_at": "2024-02-05T08:31:08.006Z"
            },
            "components": [
                {
                    "id": "8l4ygp009s5s",
                    "name": "Git Operations",
                    "status": "operational",
                    "created_at": "2017-01-31T20:05:05.370Z",
                    "updated_at": "2024-01-09T14:32:53.456Z",
                    "position": 1,
                    "description": "Performance of git clones, pulls, pushes, and associated operations",
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "brv1bkgrwx7q",
                    "name": "API Requests",
                    "status": "operational",
                    "created_at": "2017-01-31T20:01:46.621Z",
                    "updated_at": "2024-01-09T14:24:13.860Z",
                    "position": 2,
                    "description": "Requests for GitHub APIs",
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "4230lsnqdsld",
                    "name": "Webhooks",
                    "status": "operational",
                    "created_at": "2019-11-13T18:00:24.256Z",
                    "updated_at": "2024-01-09T14:20:01.432Z",
                    "position": 3,
                    "description": "Real time HTTP callbacks of user-generated and system events",
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "0l2p9nhqnxpd",
                    "name": "Visit www.githubstatus.com for more information",
                    "status": "operational",
                    "created_at": "2018-12-05T19:39:40.838Z",
                    "updated_at": "2022-09-07T00:08:33.519Z",
                    "position": 4,
                    "description": None,
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "kr09ddfgbfsf",
                    "name": "Issues",
                    "status": "operational",
                    "created_at": "2017-01-31T20:01:46.638Z",
                    "updated_at": "2024-01-09T14:24:02.127Z",
                    "position": 5,
                    "description": "Requests for Issues on GitHub.com",
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "hhtssxt0f5v2",
                    "name": "Pull Requests",
                    "status": "operational",
                    "created_at": "2020-09-02T15:39:06.329Z",
                    "updated_at": "2024-01-09T14:38:57.170Z",
                    "position": 6,
                    "description": "Requests for Pull Requests on GitHub.com",
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "br0l2tvcx85d",
                    "name": "Actions",
                    "status": "operational",
                    "created_at": "2019-11-13T18:02:19.432Z",
                    "updated_at": "2024-01-21T06:19:52.242Z",
                    "position": 7,
                    "description": "Workflows, Compute and Orchestration for GitHub Actions",
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "st3j38cctv9l",
                    "name": "Packages",
                    "status": "operational",
                    "created_at": "2019-11-13T18:02:40.064Z",
                    "updated_at": "2024-01-09T14:37:18.000Z",
                    "position": 8,
                    "description": "API requests and webhook delivery for GitHub Packages",
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "vg70hn9s2tyj",
                    "name": "Pages",
                    "status": "operational",
                    "created_at": "2017-01-31T20:04:33.923Z",
                    "updated_at": "2024-01-09T14:16:28.324Z",
                    "position": 9,
                    "description": "Frontend application and API servers for Pages builds",
                    "showcase": False,
                    "start_date": None,
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "h2ftsgbw7kmk",
                    "name": "Codespaces",
                    "status": "operational",
                    "created_at": "2021-08-11T16:02:09.505Z",
                    "updated_at": "2024-01-21T09:34:34.651Z",
                    "position": 10,
                    "description": "Orchestration and Compute for GitHub Codespaces",
                    "showcase": False,
                    "start_date": "2021-08-11",
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                },
                {
                    "id": "pjmpxvq2cmr2",
                    "name": "Copilot",
                    "status": "operational",
                    "created_at": "2022-06-21T16:04:33.017Z",
                    "updated_at": "2023-12-01T18:16:24.775Z",
                    "position": 11,
                    "description": None,
                    "showcase": False,
                    "start_date": "2022-06-21",
                    "group_id": None,
                    "page_id": "kctbh9vrtdwd",
                    "group": False,
                    "only_show_if_degraded": False
                }
            ]
        }
    elif 'v2/status.json' in url:
        res = {
            "page": {
                "id": "kctbh9vrtdwd",
                "name": "GitHub",
                "url": "https://www.githubstatus.com",
                "time_zone": "Etc/UTC",
                "updated_at": "2024-02-05T08:31:08.006Z"
            },
            "status": {
                "indicator": "none",
                "description": "All Systems Operational"
            }
        }
    else:
        res = {}

    mock_object = MagicMock()
    mock_object.json.return_value = res
    mock_object.content.return_value = str(res).encode('utf-8')
    mock_object.text.return_value = str(res)
    mock_object.status_code = 200
    return mock_object


class TestGitHubStatusL1(unittest.TestCase):

    @patch('requests.get')
    def test_github_status_all_components_functioning(self, mock_requests_get):
        mock_requests_get.side_effect = side_effect_good
        result = github_status()
        self.assertEqual(result, [])

    @patch('requests.get')
    def test_github_status_some_components_down(self, mock_requests_get):
        mock_requests_get.side_effect = side_effect_bad
        result = github_status()
        self.assertEqual(set(result), {'API', 'Management Portal'})


if __name__ == '__main__':
    unittest.main()
