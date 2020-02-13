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
    def connect_to_devices(self, testbed, p_connect = True):

        # convert from pyATS testbed to genie testbed
        # this step will be deprecated soon (and not required)
        testbed = self.parent.parameters['testbed'] = load(testbed)

        # connect to all devices in testbed in parallel
        if p_connect:
            testbed.connect()
        else:
            for device in testbed:
                try:
                    device.connect()
                except Exception:
                    logger.exception('failed to connect to device %s' 
                                     % device.name)
        
        log.debug(self.parameters)

    @aetest.subsection
    def prepare_testcases(self, testbed):
        '''
        creates a loop over the CRC_count_Check class using device name
        as the iterator
        '''
        # use device name as iterator for clarity in testcase name reporting
        aetest.loop.mark(CRC_Count_Check, 
                         device = [d.name for d in testbed])

###################################################################
#                     TESTCASES SECTION                           #
###################################################################
class CRC_Count_Check(aetest.Testcase):
    '''
    Capture Interfaces statistics on the device and tabulate
    Also look for CRC Errors. If CRC error exceeds threshold, fail
    '''

    @aetest.setup
    def setup(self, device, testbed):
        '''
        parameters
        ----------
            device: current device to check crc for (assigned by loop)
            testbed: testbed object
        '''

        log.info(banner("Gathering Interface Information from %s" 
                        % device))

        # get device by name (device is a hostname from our loop assignment)
        device = testbed.devices[device]

        if device.connected:
            self.interface_info = device.learn('interface')
        else:
            self.failed('Cannot learn %s interface information: '
                        'did not establish connectivity to device' 
                        % device.name)

    @aetest.test
    def interface_crc_counter_summary(self, device, crc_threshold = 0):
        '''
        creates and displays the CRC summary table for this device

        parameters
        ----------
            device: current device to check crc for (assigned by loop)
            crc_threshold: max crc threshold before interface check fails
        '''
        
        table_data = []
        self.failed_interfaces = {}

        for intf, data in self.interface_info.info.items():
            counters = data.get('counters')
            if counters:
                table_row = []
                if 'in_crc_errors' in counters:
                    table_row.append(device)
                    table_row.append(intf)
                    table_row.append(str(counters['in_crc_errors']))
                    if counters['in_crc_errors'] > crc_threshold:
                        table_row.append('Failed')
                        self.failed_interfaces[intf] = counters['in_crc_errors']
                    else:
                        table_row.append('Passed')

                else:
                    table_row.append(device)
                    table_row.append(intf)
                    table_row.append('N/A')
                    table_row.append('N/A')
                table_data.append(table_row)

        # display the table
        log.info(tabulate(table_data,
                          headers=['Device', 'Interface',
                                   'CRC Errors Counter',
                                   'Passed/Failed'],
                          tablefmt='orgtbl'))

        
        # should we pass or fail?
        if self.failed_interfaces:
            # loop the next test on all interfaces that fail the check
            aetest.loop.mark(self.interface_check,
                             name = self.failed_interfaces.keys())
            self.failed('Some interfaces have CRC errors')
        else:
            # skip the check interface test
            # this is a bug current in v20.1 pyats.aetest, pending fix
            # aetest.skip.affix(self.interface_check, 'no interface crc errors')
            self.passed('No interfaces have CRC errors')

    @aetest.test
    def interface_check(self, name = None, crc_threshold = 0):
        # This test has been marked for loop.  intf is the looping argument
        # this test will ONLY run if interfaces has errors

        # workaround for bug in pyATS v20.1 on skip.affix - using intf check
        if name is None:
            self.skipped('no interface crc errors')
        else:
            self.failed('Interface %s has crc errors %s (threshold %s)' 
                        % (name, self.failed_interfaces[name], crc_threshold))

if __name__ == '__main__':  # pragma: no cover
    aetest.main()