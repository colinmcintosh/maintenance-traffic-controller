#!/usr/bin/env python3

import logging
import napalm
import sys
import os


LOG = logging.getLogger(__name__)

class TrafficController(object):

	def run_command_host(self, config, vendor, hostname):
		# Sample script to demonstrate loading a config for a device.

		    """Load a config for the device."""

	    if not (os.path.exists(config_file) and os.path.isfile(config_file)):
	        msg = 'Missing or invalid config file {0}'.format(config_file)
	        raise ValueError(msg)

	    LOG.info('Loading config file {0}.'.format(config_file))

	    # Use the appropriate network driver to connect to the device:

	    driver = napalm.get_network_driver(vendor)

	    # Connect:
	    device = driver(hostname=hostname, username='user',
	                    password='pass', optional_args={'port': 12443})

	    LOG.info('Opening ...')
	    device.open()

	    LOG.info('Loading replacement candidate ...')
	    device.load_replace_candidate(filename=config_file)

	    # Note that the changes have not been applied yet. Before applying
	    # the configuration you can check the changes:
	    LOG.info('\nDiff:')
	    LOG.info(device.compare_config())

	    # You can commit or discard the candidate changes.
      	LOG.info('Committing ...')
      	device.commit_config()

	    # close the session with the device.
	    device.close()

	    LOG.info('Done.')

    def determine_template(self, vendor):
    	if vendor == "junos":
    		return "junos.j2"
    	elif vendor == "ios":
    		return "ios.j2"
    	elif vendor == "iosxr":
    		return "ios-xr.j2"

    def get_config_template(self, vendor):
        j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
        template_name = self.determine_template(vendor)
    	config = j2_env.get_template(template_name)

    def engage_maintenance_mode(self, hostname, vendor, traffic_shift_mode):
    	kwargs = {}
    	if traffic_shift_mode == "DENYALL": 
    		kwargs["DENYALL"] = True
    	elif traffic_shift_mode == "TRFENG": 
    		kwargs["TRFENG"] = True
    	self.get_config_template(vendor).render(
    		neighbor_addr=None, peer_group_name=None, IN_PEER=None, OUT_PEER=None, asn=None, **kwargs
    	)
    	self.run_command_host(config, vendor, hostname)

    def disengage_maintenance_mode(self, hostname, interface_name, traffic_shift_mode):
    	kwargs = {}
    	if traffic_shift_mode == "DENYALL": 
    		kwargs["DENYALL_disengage"] = True
    	elif traffic_shift_mode == "TRFENG": 
    		kwargs["TRFENG_disengage"] = True
    	self.get_config_template(vendor).render(
    		neighbor_addr=None, peer_group_name=None, IN_PEER=None, OUT_PEER=None, asn=None, **kwargs
    	)
    	self.run_command_host(config, vendor, hostname)
