#!/bin/env python

# To get a logger for the script
import logging

# To build the table at the end
from tabulate import tabulate

# Needed for aetest script
from pyats import aetest
from pyats.log.utils import banner

# Genie Imports
from genie.testbed import load


# Get your logger for your script
log = logging.getLogger(__name__)

###################################################################
#                  COMMON SETUP SECTION                           #
###################################################################

class common_setup(aetest.CommonSetup):
    """ Common Setup section """

    # Connect to each device in the testbed
    @aetest.subsection
    def connect(self, testbed):
        genie_testbed = load(testbed)
        self.parent.parameters['testbed'] = genie_testbed
        device_list = []
        for device in genie_testbed.devices.values():
            log.info(banner(
                f"Connect to device '{device.name}'"))
            try:
                device.connect()
                device_list.append(device)
            except Exception as e:
                log.info(f"Failed to establish connection to '{device.name}'")

        self.parent.parameters.update(dev=device_list)
        log.debug(self.parent.parameters)

    @aetest.subsection
    def create_testcases(self):
        #below creates a loop over the CRC_count_Check Class using dev as the iterator
        aetest.loop.mark(CRC_count_Check, dev=self.parent.parameters['dev'])

class CRC_count_Check(aetest.Testcase):
    @aetest.setup
    def setup(self, dev):
        #Setup has been marked for looping in Common Setup(create_testcases) with the argument dev
        #dev is the list of devices in the current testbed
        log.info(banner(f"Gathering Interface Information from {dev.name}"))
        self.interface_info = dev.learn('interface')


        list_of_interfaces=self.interface_info.info.keys()
        mega_dict = {}
        mega_dict[dev.name] = {}
        mega_tabular = []
        passing=0


        for ints, props in self.interface_info.info.items():
            counters = props.get('counters')
            if counters:
                smaller_tabular = []
                if 'in_crc_errors' in counters:
                    mega_dict[dev.name][ints] = counters['in_crc_errors']
                    smaller_tabular.append(dev.name)
                    smaller_tabular.append(ints)
                    smaller_tabular.append(str(counters['in_crc_errors']))
                    if counters['in_crc_errors']:
                        smaller_tabular.append('Failed')
                        passing=1
                    else:
                        smaller_tabular.append('Passed')

                else:
                    mega_dict[dev.name][ints] = None
                    smaller_tabular.append(dev.name)
                    smaller_tabular.append(ints)
                    smaller_tabular.append('N/A')
                    smaller_tabular.append('N/A')
            mega_tabular.append(smaller_tabular)
        mega_tabular.append(['-' * sum(len(i) for i in smaller_tabular)])

        #pass megadict to interface test function
        self.parent.parameters.update(mega=mega_dict[dev.name])
        #pass megatable list to table_display test function
        self.parent.parameters.update(megatable=mega_tabular)
        #pass passing variable to table_display function in order indicate pass or fail - 0=pass 1=fail
        self.parent.parameters.update(passing=passing)

        aetest.loop.mark(self.interface_check, intf=list_of_interfaces)

    @aetest.test
    def table_display(self):
        log.info(tabulate(self.parent.parameters['megatable'],
                          headers=['Device', 'Interface',
                                   'CRC Errors Counter',
                                   'Passed/Failed'],
                          tablefmt='orgtbl'))

        if self.parent.parameters['passing']==1:
            self.failed('Some interfaces have CRC errors')
        else:
            self.passed

    @aetest.test
    def interface_check(self, intf):
        # This test has been marked for loop.  intf is the looping argument (list of interfaces)
        # Thus this test is run for each interface in the intf list.
        for int, errors in self.parent.parameters['mega'].items():
            if errors:
                self.failed(f'Interface {int} has crc errors {errors}')
            else:
                self.passed(f'No errors on {int}')


