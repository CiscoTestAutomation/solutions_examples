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
from genie.utils.config import Config
from genie.utils.diff import Diff
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

class running_vs_startup(aetest.Testcase):
    @aetest.setup
    def setup(self, testbed):
        """Parse config archive from the testbed devices."""
        self.configs = {}
        for device_name, device in testbed.devices.items():
            # Only attempt to learn details on supported network operation systems
            # (does not work for IOSXR)
            if device.os in ("ios", "iosxe", "nxos"):
                logger.info(f"{device_name} connected status: {device.connected}")
                logger.info(f"Learning configs for {device_name}")
                startup = device.execute("show startup")
                startup_config = Config(startup)
                startup_config.tree()
                self.configs[device_name] = {}
                self.configs[device_name]['startup'] = startup_config.config
                running = device.execute("show running")
                running_config = Config(running)
                running_config.tree()
                self.configs[device_name]['running'] = running_config.config

    @aetest.test
    def test(self, steps):
        # Loop over every device with learnt configs
        for device_name, config in self.configs.items():
            with steps.start(
                f"Looking for running/startup diff on {device_name}", continue_=True
            ) as device_step:
                # Get rid of certificate comparison, as "service private-config-encryption" won't show them
                exclusion = []
                for key in config['startup'].keys():
                    if key.startswith('crypto pki certificate') or key.startswith('crypto pki trust') or key.startswith('Using '):
                        exclusion.append(key)
                for key in config['running'].keys():
                    if key.startswith('Building configuration...') or key.startswith('Current configuration :'):
                        exclusion.append(key)
                # Compare configs
                diff = Diff(config['startup'], config['running'], exclude=exclusion)
                diff.findDiff()
                if len(str(diff)) > 0:
                    device_step.failed(
                        f'Device {device_name} has the following config difference:\n{str(diff)}')

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
