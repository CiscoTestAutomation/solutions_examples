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

# List of addresses to ping:
ping_list = ['208.67.222.222', '8.8.8.8', '1.1.1.1']

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

class ping_class(aetest.Testcase):
    @aetest.setup
    def setup(self, testbed):
        """ Make sure devices can ping a list of addresses. """
        self.ping_results = {}
        for device_name, device in testbed.devices.items():
            # Only attempt to ping on supported network operation systems
            if device.os in ("ios", "iosxe", "iosxr", "nxos"):
                logger.info(f"{device_name} connected status: {device.connected}")
                self.ping_results[device_name] = {}
                for ip in ping_list:
                    logger.info(f"Pinging {ip} from {device_name}")
                    try:
                        ping = device.ping(ip)
                        pingSuccessRate = ping[(ping.find('percent')-4):ping.find('percent')].strip()
                        try:
                            self.ping_results[device_name][ip] = int(pingSuccessRate)
                        except:
                            self.ping_results[device_name][ip] = 0
                    except:
                        self.ping_results[device_name][ip] = 0

    @aetest.test
    def test(self, steps):
        # Loop over every ping result
        for device_name, ips in self.ping_results.items():
            with steps.start(
                f"Looking for ping failures {device_name}", continue_=True
            ) as device_step:
                # Loop over every ping result
                for ip in ips:
                    with device_step.start(
                        f"Checking Ping from {device_name} to {ip}", continue_=True
                    ) as ping_step:
                        if ips[ip] < 100:
                            device_step.failed(
                            f'Device {device_name} had {ips[ip]}% success pinging {ip}')

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
