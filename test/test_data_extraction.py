from datetime import date, timedelta, datetime
import unittest

from health_data_processor import load_tracker, process_new_data

# TODO: Fix unit tests to ensure data_tracker.json get updated correctly

class TestDataPull(unittest.TestCase):

    def test_process_new_data(self):
        mock_tracker_data = {
                               "sleep_time": {
                                    "endpoint": "/v2/sandbox/usercollection/sleep_time",
                                    "last_indexed": "2024-12-28"
                                }
                            }
        for i in range(10):
            with self.subTest(iteration=i):  # Isolate each loop iteration

                last_indexed = mock_tracker_data["sleep_time"]["last_indexed"]
                year, month , day = map(int, last_indexed.split("-"))
                date_obj = date(year, month, day)
                date_to_collect_from = date_obj + timedelta(1)
                print(date_to_collect_from)
                endpoint = mock_tracker_data["sleep_time"]["endpoint"]
                mock_tracker_data["sleep_time"]["last_indexed"] = str(date_to_collect_from)
                self.assertEqual(mock_tracker_data["sleep_time"]["last_indexed"], str(date_to_collect_from))
    
    def test_muliple_pulls(self):
        mock_tracker_data = {   
                                "daily_cardiovascular_age": {
                                    "endpoint": "/v2/sandbox/usercollection/daily_cardiovascular_age",
                                    "last_indexed": "2024-12-27"
                                },
                                "daily_activity": {
                                    "endpoint": "/v2/sandbox/usercollection/daily_activity",
                                    "last_indexed": "2024-12-27"
                                },
                                "vO2_max": {
                                    "endpoint": "/v2/sandbox/usercollection/vO2_max",
                                    "last_indexed": "2024-12-27"
                                }
                            }
        for i in range(10):
            for i, key in enumerate(mock_tracker_data.keys()):
                with self.subTest(iteration=i):
                    last_indexed = mock_tracker_data[key]["last_indexed"]
                    year, month , day = map(int, last_indexed.split("-"))
                    date_obj = date(year, month, day)
                    date_to_collect_from = date_obj + timedelta(1)
                    endpoint = mock_tracker_data[key]["endpoint"]
                    mock_tracker_data[key]["last_indexed"] = str(date_to_collect_from)
                    self.assertEqual(mock_tracker_data[key]["last_indexed"], str(date_to_collect_from))
                    print(mock_tracker_data[key]["last_indexed"])


if __name__ == '__main__':
    unittest.main()