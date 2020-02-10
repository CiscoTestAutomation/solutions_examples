#!/bin/env python

# To get a logger for the script
import logging

# To build the table at the end
from tabulate import tabulate

# Needed for aetest script
from ats import aetest
from ats.log.utils import banner

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
            except Exception as e:
                self.failed(f"Failed to establish connection to '{device.name}'")

            device_list.append(device)

        # Pass list of devices the to testcases
        self.parent.parameters.update(dev=device_list)
        print(self.parent.parameters)


###################################################################
#                     TESTCASES SECTION                           #
###################################################################

# Testcase name : Check for CRC errors
class CRC_count_check(aetest.Testcase):
    """ This is user Testcases section """

    # First test section
    @ aetest.test
    def learn_interfaces(self):

        self.all_interfaces = {}
        for dev in self.parent.parameters['dev']:
            log.info(banner(f"Gathering Interface Information from {dev.name}"))
            intf = dev.learn('interface')
            self.all_interfaces[dev.name] = intf.info

    # Second test section
    @ aetest.test
    def check_CRC(self):

        mega_dict = {}
        mega_tabular = []
        for device, ints in self.all_interfaces.items():
            mega_dict[device] = {}
            for name, props in ints.items():
                counters = props.get('counters')
                if counters:
                    smaller_tabular = []
                    if 'in_crc_errors' in counters:
                        mega_dict[device][name] = counters['in_crc_errors']
                        smaller_tabular.append(device)
                        smaller_tabular.append(name)
                        smaller_tabular.append(str(counters['in_crc_errors']))
                        if counters['in_crc_errors']:
                            smaller_tabular.append('Failed')
                        else:
                            smaller_tabular.append('Passed')
                    else:
                        mega_dict[device][name] = None
                        smaller_tabular.append(device)
                        smaller_tabular.append(name)
                        smaller_tabular.append('N/A')
                        smaller_tabular.append('N/A')
                mega_tabular.append(smaller_tabular)

        mega_tabular.append(['-'*sum(len(i) for i in smaller_tabular)])

        log.info(tabulate(mega_tabular,
                          headers=['Device', 'Interface',
                                   'CRC Errors Counter',
                                   'Passed/Failed'],
                          tablefmt='orgtbl'))

        for dev in mega_dict:
            for intf in mega_dict[dev]:
                if mega_dict[dev][intf]:
                    self.failed(f"{dev}: {intf} CRC ERRORS: {mega_dict[dev][intf]}")

        self.passed("All devices' interfaces CRC ERRORS Count is: 'Zero'")

# #####################################################################
# ####                       COMMON CLEANUP SECTION                 ###
# #####################################################################


# This is how to create a CommonCleanup
# You can have 0 , or 1 CommonCleanup.
# CommonCleanup can be named whatever you want :)
class common_cleanup(aetest.CommonCleanup):
    """ Common Cleanup for Sample Test """

    # CommonCleanup follow exactly the same rule as CommonSetup regarding
    # subsection
    # You can have 1 to as many subsections as wanted
    # here is an example of 1 subsection

    # @aetest.subsection
    # def clean_everything(self):
    #     """ Common Cleanup Subsection """
    #     log.info("Aetest Common Cleanup ")
    @aetest.subsection

    def disconnect(self):
        log.info("Aetest Common Cleanup disconnecting devices")
        for dev in self.parent.parameters['dev']:
            dev.disconnect()


if __name__ == '__main__':  # pragma: no cover
    aetest.main()