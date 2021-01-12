import unittest

from lifeguard_tinydb.settings import (
    SETTINGS_MANAGER,
    LIFEGUARD_TINYDB_LOCATION,
)


class SettingsTest(unittest.TestCase):
    def test_lifeguard_tinydb_database(self):
        self.assertEqual(LIFEGUARD_TINYDB_LOCATION, "lifeguard.json")
        self.assertEqual(
            SETTINGS_MANAGER.settings["LIFEGUARD_TINYDB_LOCATION"]["description"],
            "Path to database file",
        )
