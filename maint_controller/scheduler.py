#!/usr/bin/env python3
import logging
import os
import time
from datetime import datetime, timedelta

from tinydb import TinyDB, Query

from maint_controller.circuitdb import CircuitDB
from maint_controller.config import config
from maint_controller.controller import TrafficController


LOG = logging.getLogger(__name__)


class MaintenanceScheduler(object):

    def __init__(self):
        self._traffic_controller = TrafficController()
        self._cdb = CircuitDB()

    def schedule_db(self):
        os.makedirs(config.SCHEDULE_FILE_PATH, exist_ok=True)
        return TinyDB(os.path.join(config.SCHEDULE_FILE_PATH, config.SCHEDULE_FILE_NAME))

    def get_maintenance_events_starting_soon(self):
        LOG.info("Checking for events that are starting soon...")
        Event = Query()
        now = datetime.now()
        events_starting_soon = []
        with self.schedule_db() as db:
            results = db.search((~ Event.maintenance_engaged.exists()) | (Event.maintenance_engaged != True))
            for event in results:
                event_start_time = datetime.strptime(event["start_time"], "%Y-%m-%dT%H:%M:%S")
                if now - event_start_time < timedelta(minutes=5):
                    events_starting_soon.append(event)
        return events_starting_soon

    def get_maintenance_events_recently_ended(self):
        LOG.info("Checking for events that recently ended...")
        Event = Query()
        now = datetime.now()
        events_recently_ended = []
        with self.schedule_db() as db:
            results = db.search(Event.maintenance_engaged == True)
            for event in results:
                event_end_time = datetime.strptime(event["end_time"], "%Y-%m-%dT%H:%M:%S")
                if now > event_end_time:
                    events_recently_ended.append(event)
        return events_recently_ended

    def mark_maintenance_mode_engaged(self, event_uuid):
        Event = Query()
        with self.schedule_db() as db:
            db.update({"maintenance_engaged": True}, Event.event_uuid == event_uuid)
        return

    def mark_maintenance_mode_disengaged(self, event_uuid):
        Event = Query()
        with self.schedule_db() as db:
            db.update({"maintenance_engaged": False}, Event.event_uuid == event_uuid)
        return

    def run(self):
        LOG.info("Starting scheduler loop")
        while True:
            self.tick()
            for _ in range(60):
                time.sleep(1)   # Less-blocking sleep

    def tick(self):
        LOG.info("Tick started.")
        events = self.get_maintenance_events_starting_soon()
        LOG.info("Found {} events that are starting soon.".format(len(events)))
        for event in events:
            cdb_entry = self._cdb.get_circuit_by_cid(cid=event["cid"])
            if not cdb_entry:
                LOG.error("No circuit information could be found for CID {}".format(event["cid"]))
                continue
            LOG.info("Engaging maintenance mode for {} {} ({})".format(cdb_entry["hostname"], cdb_entry["interface_name"], event["event_uuid"]))
            self._traffic_controller.engage_maintenance_mode(hostname=cdb_entry["hostname"], vendor=cdb_entry["vendor"], traffic_shift_mode=cdb_entry["traffic_shift_mode"])
            self.mark_maintenance_mode_engaged(event["event_uuid"])

        events = self.get_maintenance_events_recently_ended()
        LOG.info("Found {} events that recently ended.".format(len(events)))
        for event in events:
            cdb_entry = self._cdb.get_circuit_by_cid(cid=event["cid"])
            if not cdb_entry:
                LOG.error("No circuit information could be found for CID {}".format(event["cid"]))
                continue
            LOG.info("Disengaging maintenance mode for {} {} ({})".format(cdb_entry["hostname"], cdb_entry["interface_name"], event["event_uuid"]))
            self._traffic_controller.disengage_maintenance_mode(hostname=cdb_entry["hostname"], vendor=cdb_entry["vendor"], traffic_shift_mode=cdb_entry["traffic_shift_mode"])
            self.mark_maintenance_mode_disengaged(event["event_uuid"])
        LOG.info("Tick ended")
