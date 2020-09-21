"""
show_rib_table.py

Verify the RIB Tables are not empty for each VRF
This could be used post changes to verify that you've 
not dropped routes. Thresehold of zero used but can 
be changed to any value
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


class rib_checks(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        """Learn the operational state of the RIB Table"""
        self.execute_rib = {}
        self.output= {}
        for device_name, device in testbed.devices.items():
            # Only attempt to learn details on supported network operation systems
            if device.os in ("iosxr"):
                logger.info(f"{device_name} connected status: {device.connected}")
                logger.info(print(f"Running the show rib table command for {device_name}"))
                self.execute_rib[device_name] = device.execute("show rib table")
                
                
                
    
    @aetest.test
    def test(self, steps):
        for device_name, device in self.execute_rib.items():
            header = ['VRF/Table', 'SAFI', 'Table ID', ' PrfxLmt', 'PrfxCnt', 'TblVersion', 'N', 'F', 'D', 'C']
            output = self.execute_rib[device_name]
            result = parsergen.oper_fill_tabular(device_output=output, device_os='iosxr', header_fields=header, index=[0])
            output = result.entries
            logger.info(f"Structured Output from SHOW RIB TABLE \n {output} ")
            rib_bad = Dq(output).value_operator('PrfxCnt', '==', 0).reconstruct()
            if rib_bad == {}:
                self.passed(f"No issues found with the RIB all VRFS contain more than one prefix")
                    
            else: 
                self.failed(f'Some of the RIB Tables contain zero routes \n {rib_bad}')
    
        

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
