#!/usr/bin/env python3



class BaseConfig(object):

    SCHEDULE_FILE_PATH = "~/.manage-maintenance"
    SCHEDULE_FILE_NAME = "schedule.db"

    CDB_FILE_PATH = "~/.maint-traffic-controller"
    CDB_FILE_NAME = "cdb.db"


class TestConfig(BaseConfig):

    SCHEDULE_FILE_PATH = "/tmp/manage-maintenance"

    CDB_FILE_PATH = "/tmp/maint-traffic-controller"


config = BaseConfig()
