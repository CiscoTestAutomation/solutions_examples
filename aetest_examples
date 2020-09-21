"""
Verify that LPTS Policer is not dropping packets on the Control Plane
Cisco IOS-XR
Using Genie Tabular Parser
This script can be run standalone or part of a pyats job file
"""


import logging
from pyats import aetest
from genie.testbed import load
from genie import parsergen
from genie.utils import Dq
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError



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


class lpts_checks(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        self.execute_platform = {}
        self.output= {}
        for device_name, device in testbed.devices.items():
            # Only attempt to learn details on supported network operation systems
            if device.os in ("iosxr"):
                logger.info(f"{device_name} connected status: {device.connected}")
                logger.info(print(f"Running the show lpts pifib hardware police command for {device_name}"))
                self.execute_platform[device_name] = device.execute("show lpts pifib hardware police location 0/0/CPU0")
                
                
                
    
    @aetest.test
    def test(self, steps):
        for device_name, device in self.execute_platform.items():
            header=['flow_type','priority','sw_police_id','hw_policer_addr',
                 'Cur. Rate','burst','static_avgrate','avgrate_type',
                      'AggrAccepts','AggrDrops','TOS Value']
            output = self.execute_platform[device_name]
            result = parsergen.oper_fill_tabular(device_output=output, device_os='iosxr', header_fields=header, index=[0])
            output = result.entries
            logger.info(f"Structured Output from SHOW LPTS POLICER \n {output} ")
            police_drops = Dq(output).value_operator('AggrDrops', '>', 0).reconstruct()
            if police_drops == {}:
                self.passed(f"No issues found with drops on the lpts Policer")
            
            else: 
                self.failed(f'Drops found on the control plane policer on the following processes:\n {police_drops.keys()}')
    
        

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
