#!/usr/bin/env python3
import logging
import os
from datetime import datetime, timedelta

from tinydb import TinyDB

from maint_controller.config import config
from maint_controller.scheduler import MaintenanceScheduler


LOG = logging.getLogger(__name__)


class DemoFakeout(object):
    now = datetime.now()
    fake_event = {
        "subject": "Yo stuff is goin' down!",
        "start_time": (now + timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%S"),
        "end_time": (now + timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%S"),
        "cid": "ABC1234XYZ",
        "partner": "Netflix",
        "original_message": "Stuff is going down!",
        "event_uuid": "07d488fa-e755-46d9-a59b-b98c4970e4a5"
    }
    fake_circuit = {
        "cid": "ABC1234XYZ",
        "hostname": "switch01.lab.local",
        "interface_name": "Ethernet1",
        "vendor": "iosxr",
        "traffic_shift_mode": "DENYALL"
    }

    def run_fakeout(self):
        with self.schedule_db() as db:
            db.purge()
            db.insert(self.fake_event)
        with self.circuit_db() as db:
            db.purge()
            db.insert(self.fake_circuit)
        return

    def schedule_db(self):
        os.makedirs(config.SCHEDULE_FILE_PATH, exist_ok=True)
        return TinyDB(os.path.join(config.SCHEDULE_FILE_PATH, config.SCHEDULE_FILE_NAME))

    def circuit_db(self):
        os.makedirs(config.CDB_FILE_PATH, exist_ok=True)
        return TinyDB(os.path.join(config.CDB_FILE_PATH, config.CDB_FILE_NAME))


def main():
    DemoFakeout().run_fakeout()
    logging.basicConfig(level=logging.INFO)
    scheduler = MaintenanceScheduler()
    scheduler.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupt. Exiting.")
