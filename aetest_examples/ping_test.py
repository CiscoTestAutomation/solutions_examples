"""
ping_test.py

Take a list of PING Targets from a YAML file


"""

import logging
from pyats import aetest
from genie.testbed import load
import re
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from custombits import CustomBits


# create a logger for this module
logger = logging.getLogger(__name__)


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

        try:
            testbed.connect()
        except (TimeoutError, StateMachineError, ConnectionError):
            logger.error("Unable to connect to all devices")


class connectivity_status_checks(aetest.Testcase):


    @aetest.setup
    def setup(self, testbed):
        """Learn and save the interface details from the testbed devices."""
        self.execute_ping = {}
        self.output= {}
        self.cust_ping= CustomBits().ping_dest()
        for device_name, device in testbed.devices.items():
            
            if device.os in ("iosxr"):
                logger.info(f"{device_name} connected status: {device.connected}")
                logger.info(f"Running the PING command for {device_name}")
                for k,v in self.cust_ping.items():
                    vrf_name = v.get('vrf')
                    dest  = v.get('destination')
                    ping_cnt  = v.get('count')  
                    self.execute_ping[device_name, k] = device.execute(f"ping vrf {vrf_name} {dest} count {ping_cnt}")        

                



    @aetest.test
    def test(self, steps):
        for device_name, device in self.execute_ping.items():
                        with steps.start(
                            f"Running the PING command on {device_name}", continue_=True
                        ) as device_step:
            
                            output = self.execute_ping[device_name]
                            output = output.replace('\r\n','\n')
                            match = re.search(r'Success rate is (?P<rate>\d+) percent', output)
                            success_rate = match.group('rate')
                            logger.info(f' The success rate of the PING was {success_rate}')
                            if success_rate == 100:
                                
                                device_step.passed(f' No packets dropped, connectivity is good')
                                
                                
                            else:
                                device_step.failed(f'We had a problem with some of these tests')
        
            

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

    
   
