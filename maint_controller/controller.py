#!/usr/bin/env python3
import logging
import napalm
import os

from jinja2 import Environment, FileSystemLoader


LOG = logging.getLogger(__name__)


TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


class TrafficController(object):

    def run_command_host(self, config, vendor, hostname):
        """Load a config for the device."""

        # Use the appropriate network driver to connect to the device:

        driver = napalm.get_network_driver(vendor)

        # Connect:
        device = driver(hostname=hostname, username='user',
                        password='pass', optional_args={'port': 22})

        LOG.info('Opening ...')
        #device.open()

        LOG.info('Loading replacement candidate ...')
        #device.merge_candidate_config(config=config)

        # Note that the changes have not been applied yet. Before applying
        # the configuration you can check the changes:
        LOG.info('Diff: {}'.format(device.compare_config()))

        # You can commit or discard the candidate changes.
        LOG.info('Committing ...')
        #device.commit_config()

        # close the session with the device.
        #device.close()

        LOG.info('Done committing.')

    @staticmethod
    def determine_template(vendor):
        if vendor == "junos":
            return "junos.j2"
        elif vendor == "ios":
            return "ios.j2"
        elif vendor == "iosxr":
            return "ios-xr.j2"

    def get_config_template(self, vendor):
        j2_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=True)
        template_name = self.determine_template(vendor)
        config = j2_env.get_template(template_name)
        return config

    def engage_maintenance_mode(self, hostname, vendor, traffic_shift_mode):
        kwargs = {}
        if traffic_shift_mode == "DENYALL":
            kwargs["DENYALL"] = True
        elif traffic_shift_mode == "TRFENG":
            kwargs["TRFENG"] = True
        config = self.get_config_template(vendor).render(
            neighbor_addr="127.0.0.1", peer_group_name=None, IN_PEER=None, OUT_PEER=None, asn=None, **kwargs
        )
        self.run_command_host(config, vendor, hostname)
        return

    def disengage_maintenance_mode(self, hostname, vendor, traffic_shift_mode):
        kwargs = {}
        if traffic_shift_mode == "DENYALL":
            kwargs["DENYALL_disengage"] = True
        elif traffic_shift_mode == "TRFENG":
            kwargs["TRFENG_disengage"] = True
        config = self.get_config_template(vendor).render(
            neighbor_addr="127.0.0.1", peer_group_name=None, IN_PEER=None, OUT_PEER=None, asn=None, **kwargs
        )
        self.run_command_host(config, vendor, hostname)
        return
