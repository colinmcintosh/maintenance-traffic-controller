#!/usr/bin/env python3
"""Basic end to end test."""
import logging
import os
import unittest
from datetime import datetime, timedelta

from tinydb import TinyDB, Query

import maint_controller.circuitdb
import maint_controller.scheduler
from maint_controller.config import TestConfig
from maint_controller.scheduler import MaintenanceScheduler


LOG = logging.getLogger(__name__)


class TestBasicEngageEnd2End(unittest.TestCase):
    """Basic end to end test case."""

    def setUp(self):
        """Setup databases."""
        self._previous_config_scheduler = maint_controller.scheduler.config
        self._previous_config_circuits = maint_controller.circuitdb.config
        maint_controller.scheduler.config = self.config = TestConfig()
        maint_controller.circuitdb.config = self.config
        now = datetime.now()
        self.fake_event = {
            "subject": "Yo stuff is goin' down!",
            "start_time": (now + timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%S"),
            "end_time": (now + timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%S"),
            "cid": "ABC1234XYZ",
            "partner": "Netflix",
            "original_message": "Stuff is going down!",
            "event_uuid": "07d488fa-e755-46d9-a59b-b98c4970e4a5"
        }
        self.fake_circuit = {
            "cid": "ABC1234XYZ",
            "hostname": "switch01.lab.local",
            "interface_name": "Ethernet1"
        }
        with self.schedule_db() as db:
            db.purge()
            db.insert(self.fake_event)
        with self.circuit_db() as db:
            db.purge()
            db.insert(self.fake_circuit)
        return

    def tearDown(self):
        maint_controller.scheduler.config = self._previous_config_scheduler
        maint_controller.circuitdb.config = self._previous_config_circuits

    def schedule_db(self):
        os.makedirs(self.config.SCHEDULE_FILE_PATH, exist_ok=True)
        return TinyDB(os.path.join(self.config.SCHEDULE_FILE_PATH, self.config.SCHEDULE_FILE_NAME))

    def circuit_db(self):
        os.makedirs(self.config.CDB_FILE_PATH, exist_ok=True)
        return TinyDB(os.path.join(self.config.CDB_FILE_PATH, self.config.CDB_FILE_NAME))

    def test_scheduler_full_tick(self):
        """Test notification."""
        scheduler = MaintenanceScheduler()
        scheduler.tick()
        with self.schedule_db() as db:
            Event = Query()
            results = db.search(Event.event_uuid == self.fake_event["event_uuid"])
        self.assertTrue(len(results) > 0)
        self.assertTrue(results[0].get("maintenance_engaged", False))


def main():
    """Main."""
    unittest.main()


if __name__ == '__main__':
    main()
