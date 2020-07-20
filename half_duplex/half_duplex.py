"""
half_duplex.py
"""
# see https://pubhub.devnetcloud.com/media/pyats/docs/aetest/index.html
# for documentation on pyATS test scripts

__author__ = "Oren Brigg"
__copyright__ = "Copyright (c) 2020, Cisco Systems Inc."
__contact__ = ["obrigg@cisco.com"]
__credits__ = ["hapresto@cisco.com"]
__version__ = 1.0

import logging

from pyats import aetest
from genie.testbed import load
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError

# create a logger for this module
logger = logging.getLogger(__name__)

###################################################################
#                  COMMON SETUP SECTION                           #
###################################################################

class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def load_testbed(self, testbed):
        # Convert pyATS testbed to Genie Testbed
        logger.info(
            "Converting pyATS testbed to Genie Testbed to support pyATS Library features"
        )
        testbed = load(testbed)
        self.parent.parameters.update(testbed=testbed)

    @aetest.subsection
    def connect(self, testbed):
        """
        establishes connection to all your testbed devices.
        """
        # make sure testbed is provided
        assert testbed, "Testbed is not provided!"

        # connect to all testbed devices
        #   By default ANY error in the CommonSetup will fail the entire test run
        #   Here we catch common exceptions if a device is unavailable to allow test to continue
        try:
            testbed.connect()
        except (TimeoutError, StateMachineError, ConnectionError):
            logger.error("Unable to connect to all devices")

###################################################################
#                     TESTCASES SECTION                           #
###################################################################

class interface_duplex(aetest.Testcase):
    @aetest.setup
    def setup(self, testbed):
        """Learn and save the interface details from the testbed devices."""
        self.learnt_interfaces = {}
        for device_name, device in testbed.devices.items():
            # Only attempt to learn details on supported network operation systems
            if device.os in ("ios", "iosxe", "iosxr", "nxos"):
                logger.info(f"{device_name} connected status: {device.connected}")
                logger.info(f"Learning Interfaces for {device_name}")
                self.learnt_interfaces[device_name] = device.learn("interface").info

    @aetest.test
    def test(self, steps):
        # Loop over every device with learnt interfaces
        for device_name, interfaces in self.learnt_interfaces.items():
            with steps.start(
                f"Looking for half-duplex Interfaces on {device_name}", continue_=True
            ) as device_step:

                # Loop over every interface that was learnt
                for interface_name, interface in interfaces.items():
                    with device_step.start(
                        f"Checking Interface {interface_name}", continue_=True
                    ) as interface_step:

                        # Verify that this interface has "duplex_mode" (Virtual interfaces Lack duplex)
                        if "duplex_mode" in interface.keys():
                            if interface['duplex_mode'] == 'half':
                                interface_step.failed(
                                    f'Device {device_name} Interface {interface_name} is in half-duplex mode')
                        else:
                            # If the interface has no duplex, mark as skipped
                            interface_step.skipped(
                                f"Device {device_name} Interface {interface_name} has no duplex"
                            )


class CommonCleanup(aetest.CommonCleanup):
    """CommonCleanup Section

    < common cleanup docstring >

    """

    # uncomment to add new subsections
    # @aetest.subsection
    # def subsection_cleanup_one(self):
    #     pass


if __name__ == "__main__":
    # for stand-alone execution
    import argparse
    from pyats import topology

    # from genie.conf import Genie

    parser = argparse.ArgumentParser(description="standalone parser")
    parser.add_argument(
        "--testbed",
        dest="testbed",
        help="testbed YAML file",
        type=topology.loader.load,
        # type=Genie.init,
        default=None,
    )

    # do the parsing
    args = parser.parse_known_args()[0]

    aetest.main(testbed=args.testbed)
