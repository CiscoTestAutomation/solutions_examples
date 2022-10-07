"""Implementation Hostname triggers"""

import logging
from ruamel.yaml import YAML
from pyats import aetest
from genie.harness.base import Trigger
import re
import ipaddress
from pathlib import Path

log = logging.getLogger(__name__)

class TriggerAudit(Trigger):

    @aetest.test
    def Connect_to_Device(self, uut, steps, message):
        log.info("Test case steps:\n{msg}".format(msg=message))

        with steps.start('Connect to test device') as step:
            failed=False
            try:
                uut.connect(connection_timeout=5)
            except:
                failed=True
                log.error('Failed connection #1')
            if failed:
                try:
                    uut.connect(connection_timeout=5)
                except:
                    # If Connection fail 2 times for vRouter, go to cleanup blocking next Tests and continuing
                    # with the next device on Trigger Datafile
                    self.failed('Connection failed', goto = ['cleanup'])
            else:
                step.passed('Connection sucess')

    @aetest.test
    def Test_ISIS(self, uut, steps, isis_interfaces):
        with steps.start('ISIS Check') as step:
            output = uut.parse('show isis neighbors')
            isis_int_dict = output['isis']['pyATS']['vrf']['default']['interfaces']
            for interface in isis_interfaces:
                if interface in isis_int_dict.keys():
                    log.info('Interface: {} found on ISIS neighbors'.format(interface))
                else:
                    step.failed('Interface: {} not found on ISIS neighbors'.format(interface))
                for neighbor in isis_int_dict[interface]['neighbors'].keys():
                    if isis_int_dict[interface]['neighbors'][neighbor]['state'] == 'Up':
                        log.info('Interface: {} has neighbor {}, in Up State'.format(interface,neighbor))
                    else:
                        step.failed('Interface: {} is not on Up State'.format(interface))
            step.passed('All interfaces found on ISIS neighbor table on Up state')

