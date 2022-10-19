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
    def Test_BGP(self, uut, steps, prefix_threshold):
        with steps.start('Check BGP ipv4 unicast prefixes', continue_=True) as step:
            output = uut.parse('show bgp ipv4 unicast summary')
            neighbor_dict = output['instance']['all']['vrf']['default']['neighbor']
            for neighbor in neighbor_dict.keys():
                if int(neighbor_dict[neighbor]['address_family']['ipv4 unicast']['state_pfxrcd']) > prefix_threshold:
                    continue
                else:
                    step.failed('0 Prefixes received from neighbor: {}'.format(neighbor))
            step.passed('Prefixes received for AFI on all neighbors')

        with steps.start('Check BGP ipv6 unicast prefixes', continue_=True) as step:
            output = uut.parse('show bgp ipv6 unicast summary')
            neighbor_dict = output['instance']['all']['vrf']['default']['neighbor']
            for neighbor in neighbor_dict.keys():
                if int(neighbor_dict[neighbor]['address_family']['ipv6 unicast']['state_pfxrcd']) > prefix_threshold:
                    continue
                else:
                    step.failed('0 Prefixes received from neighbor: {}'.format(neighbor))
            step.passed('Prefixes received for AFI on all neighbors')

        with steps.start('Check BGP vpnv4 unicast prefixes', continue_=True) as step:
            output = uut.parse('show bgp vpnv4 unicast summary')
            neighbor_dict = output['instance']['all']['vrf']['default']['neighbor']
            for neighbor in neighbor_dict.keys():
                if int(neighbor_dict[neighbor]['address_family']['vpnv4 unicast']['state_pfxrcd']) > prefix_threshold:
                    continue
                else:
                    step.failed('0 Prefixes received from neighbor: {}'.format(neighbor))
            step.passed('Prefixes received for AFI on all neighbors')

        with steps.start('Check BGP vpnv6 unicast prefixes') as step:
            output = uut.parse('show bgp vpnv6 unicast summary')
            neighbor_dict = output['instance']['all']['vrf']['default']['neighbor']
            for neighbor in neighbor_dict.keys():
                if int(neighbor_dict[neighbor]['address_family']['vpnv6 unicast']['state_pfxrcd']) > prefix_threshold:
                    continue
                else:
                    step.failed('0 Prefixes received from neighbor: {}'.format(neighbor))
            step.passed('Prefixes received for AFI on all neighbors')