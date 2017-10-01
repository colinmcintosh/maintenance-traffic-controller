#!/usr/bin/env python3
import logging
import os
from collections import namedtuple

from tinydb import TinyDB, Query

from maint_controller.config import config


LOG = logging.getLogger(__name__)


Circuit = namedtuple("Circuit", ("cid", "hostname", "interface_name"))


class CircuitDB(object):

    def __init__(self):
        pass

    def db(self):
        os.makedirs(config.CDB_FILE_PATH, exist_ok=True)
        return TinyDB(os.path.join(config.CDB_FILE_PATH, config.CDB_FILE_NAME))

    def get_circuit_by_cid(self, cid):
        with self.db() as db:
            results = db.search(Query().cid == cid)
        try:
            return results[0]
        except IndexError:
            return None
