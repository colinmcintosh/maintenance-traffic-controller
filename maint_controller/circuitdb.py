#!/usr/bin/env python3

import os
from collections import namedtuple

from tinydb import TinyDB, Query

from maint_controller.config import config


Circuit = namedtuple("Circuit", ("cid", "hostname", "interface_name"))


class CircuitDB(object):

    def __init__(self):
        pass

    def db(self):
        return TinyDB(os.path.join(config.CDB_FILE_PATH, config.CDB_FILE_NAME))

    def get_circuit_by_cid(self, cid):
        with self.db() as db:
            results = db.search(Query().cid == cid)
        return results

