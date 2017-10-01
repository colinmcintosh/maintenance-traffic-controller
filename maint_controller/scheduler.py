#!/usr/bin/env python3
# Copyright 2017 Netflix
import os
import time
from datetime import datetime, timedelta

from tinydb import TinyDB, Query

from maint_controller.circuitdb import CircuitDB
from maint_controller.config import config
from maint_controller.controller import TrafficController


class MaintenanceScheduler(object):

    def __init__(self):
        self._traffic_controller = TrafficController()
        self._cdb = CircuitDB()

    def schedule_db(self):
        return TinyDB(os.path.join(config.CDB_FILE_PATH, config.CDB_FILE_NAME))

    def load_events_from_database(self):
        pass

    def get_maintenance_events_starting_soon(self):
        Event = Query()
        now = datetime.now()
        events_starting_soon = []
        with self.schedule_db() as db:
            results = db.search(Event.maintenance_engaged is not True)
            for event in results:
                event_start_time = datetime.strptime(event["start_time"], "%Y-%m-%dT%H:%M:%s")
                if now - event_start_time < timedelta(minutes=5):
                    events_starting_soon.append(event)
        return events_starting_soon

    def get_maintenance_events_recently_ended(self):
        Event = Query()
        now = datetime.now()
        events_recently_ended = []
        with self.schedule_db() as db:
            results = db.search(Event.maintenance_engaged is True)
            for event in results:
                event_end_time = datetime.strptime(event["end_time"], "%Y-%m-%dT%H:%M:%s")
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
        while True:
            time.sleep(60)
            events = self.get_maintenance_events_starting_soon()
            for event in events:
                cdb_entry = self._cdb.get_circuit_by_cid(cid=event["cid"])
                self._traffic_controller.engage_maintenance_mode(hostname=cdb_entry["hostname"], interface_name=cdb_entry["interface_name"])
                self.mark_maintenance_mode_engaged(event["event_uuid"])

            events = self.get_maintenance_events_recently_ended()
            for event in events:
                cdb_entry = self._cdb.get_circuit_by_cid(cid=event["cid"])
                self._traffic_controller.disengage_maintenance_mode(hostname=cdb_entry["hostname"], interface_name=cdb_entry["interface_name"])
                self.mark_maintenance_mode_disengaged(event["event_uuid"])
