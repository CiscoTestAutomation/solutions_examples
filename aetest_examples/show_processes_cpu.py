"""
show_processes_cpu.py

Verify the CPU Utlisation is not exceeding 75 percent for more than 5 minutes

"""
# see https://pubhub.devnetcloud.com/media/pyats/docs/aetest/index.html
# for documentation on pyATS test scripts

import logging
from ttp import ttp
from pyats import aetest
from genie.testbed import load
from rich.logging import RichHandler
from genie import parsergen
import re
from genie.utils import Dq
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError

# create a logger for this module
logger = logging.getLogger(__name__)
FORMAT = "%(message)s"
logger = logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
logger = logging.getLogger("rich")
path_store = 'some value'

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
    def set_store_num(self, store):
        aetest.loop.mark
        
class CPU_utilisation_checks(aetest.Testcase):
    """
    Check the CPU Utilisation of all the devices in the testbed.yaml
    Report a failure if a CPU Process exceeds 75 Percent for more
    than 5 minutes

    """

    # List of counters keys to check for errors
    #   Model details: https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/_models/interface.pdf
    @aetest.setup
    def setup(self, testbed):
        """Check the Network OS matches the Testbed.yaml file"""
        self.execute_cpu = {}
        self.output= {}

        
        for device_name, device in testbed.devices.items():
            # Only attempt to learn details on supported network operation systems
            if device.os in ("iosxr"):
                logger.info(f"{device_name} connected status: {device.connected}")
                logger.info(f"Running the show processes cpu command for {device_name}")
                self.execute_cpu[device_name] = device.execute("show processes cpu")
                
    
    @aetest.test
    def test(self, steps):
        
        print(path_store)
        for device_name, device in self.execute_cpu.items():
            header = ['PID', '1Min', '5Min', '15Min', 'Process']
            output= self.execute_cpu[device_name]
            output = re.sub('%',' ', output)
            result = parsergen.oper_fill_tabular(device_output=output, device_os='iosxr', header_fields=header, index=[0])
            output=result.entries
            cpu_bad = Dq(output).value_operator('5Min', '>=', 75).reconstruct()
            process_id = str(cpu_bad.keys())
            if cpu_bad != {}:
                self.failed(f'Very High 5 Minute CPU detected on {device} with the following Process ID {process_id}')
                

            else:
                self.passed(f'No issues found with the CPU Utilisation on {device_name}') 


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

