#!/usr/bin/env python3

import logging

from maint_controller.scheduler import MaintenanceScheduler


LOG = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    scheduler = MaintenanceScheduler()
    scheduler.run()


if __name__ == "__main__":
    main()
