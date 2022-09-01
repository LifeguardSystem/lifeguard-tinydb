import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from lifeguard.notifications import NotificationStatus
from lifeguard.validations import ValidationResponse
from tinydb import Query

from lifeguard_tinydb.repositories import (
    TinyDBNotificationRepository,
    TinyDBValidationRepository,
)


class TestTinyDBValidationRepository(unittest.TestCase):
    @patch("lifeguard_tinydb.repositories.DATABASE")
    def setUp(self, mock_database):
        self.table = MagicMock(name="validations")
        mock_database.table.return_value = self.table
        self.repository = TinyDBValidationRepository()

    def test_fetch_last_validation_result_none(self):
        validation_name = "validation"
        self.table.get.return_value = None

        result = self.repository.fetch_last_validation_result(validation_name)

        self.assertIsNone(result)
        self.table.get.assert_called_with(Query().validation_name == "validation")

    def test_fetch_last_validation_result_not_none(self):
        validation_name = "validation"
        self.table.get.return_value = {
            "validation_name": "validation",
            "status": "status",
            "details": "details",
            "settings": "settings",
            "last_execution": "2020-11-19 00:00",
        }

        result = self.repository.fetch_last_validation_result(validation_name)

        self.assertEqual(result.status, "status")
        self.assertEqual(result.details, "details")
        self.assertEqual(result.settings, "settings")
        self.assertEqual(result.last_execution, datetime(2020, 11, 19))
        self.table.get.assert_called_with(Query().validation_name == "validation")

    def test_fetch_all_validation_results_not_none(self):
        self.table.all.return_value = [
            {
                "validation_name": "validation",
                "status": "status",
                "details": "details",
                "settings": "settings",
                "last_execution": "2020-11-19 00:00",
            }
        ]

        result = self.repository.fetch_all_validation_results()

        self.assertEqual(result[0].validation_name, "validation")
        self.assertEqual(result[0].status, "status")
        self.assertEqual(result[0].details, "details")
        self.assertEqual(result[0].settings, "settings")
        self.assertEqual(result[0].last_execution, datetime(2020, 11, 19))
        self.table.all.assert_called()

    def test_save_validation_result_create(self):
        self.table.count.return_value = 0
        response = ValidationResponse("name", "status", {})

        self.repository.save_validation_result(response)

        self.table.insert.assert_called_with(
            {
                "validation_name": "name",
                "status": "status",
                "details": {},
                "settings": None,
                "last_execution": None,
            }
        )

    def test_save_validation_result_update(self):
        self.table.count.return_value = 1
        response = ValidationResponse(
            "name", "status", {}, last_execution=datetime(2021, 1, 21)
        )

        self.repository.save_validation_result(response)

        self.table.update.assert_called_with(
            {
                "validation_name": "name",
                "status": "status",
                "details": {},
                "settings": None,
                "last_execution": "2021-01-21 00:00",
            },
            Query().validation_name == "name",
        )


class TestTinyDBNotificationRepository(unittest.TestCase):
    @patch("lifeguard_tinydb.repositories.DATABASE")
    def setUp(self, mock_database):
        self.table = MagicMock(name="notifications")
        mock_database.table.return_value = self.table
        self.repository = TinyDBNotificationRepository()

    def test_fetch_last_notification_for_a_validation_is_none(self):
        validation_name = "notification"
        self.table.get.return_value = None

        result = self.repository.fetch_last_notification_for_a_validation(
            validation_name
        )

        self.assertIsNone(result)
        self.table.get.assert_called_with(
            (Query().validation_name == validation_name) & (Query().is_opened == True)
        )

    def test_fetch_last_notification_for_a_validation_not_none(self):
        validation_name = "validation"
        self.table.get.return_value = {
            "thread_ids": {},
            "is_opened": True,
            "options": {},
            "last_notification": "2020-11-19 00:00",
        }

        result = self.repository.fetch_last_notification_for_a_validation(
            validation_name
        )

        self.assertEqual(result.thread_ids, {})
        self.assertEqual(result.is_opened, True)
        self.assertEqual(result.options, {})
        self.assertEqual(result.last_notification, datetime(2020, 11, 19))
        self.table.get.assert_called_with(
            (Query().validation_name == validation_name) & (Query().is_opened == True)
        )

    @patch("lifeguard.notifications.datetime")
    def test_save_last_notification_for_a_validation_create(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2020, 12, 31)

        self.table.count.return_value = 0
        notification_status = NotificationStatus("name", "status", {})

        self.repository.save_last_notification_for_a_validation(notification_status)

        self.table.insert.assert_called_with(
            {
                "validation_name": "name",
                "thread_ids": "status",
                "is_opened": True,
                "options": {},
                "last_notification": "2020-12-31 00:00",
            }
        )

    @patch("lifeguard.notifications.datetime")
    def test_save_last_notification_for_a_validation_update(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2020, 12, 31)

        self.table.count.return_value = 1
        notification_status = NotificationStatus("name", {}, {})

        self.repository.save_last_notification_for_a_validation(notification_status)

        self.table.update.assert_called_with(
            {
                "validation_name": "name",
                "thread_ids": {},
                "is_opened": True,
                "options": {},
                "last_notification": "2020-12-31 00:00",
            },
            (Query().validation_name == "name") & (Query().is_opened == True),
        )
