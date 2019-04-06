# To run the job:
# pyats run job BGP_check_job.py --testbed-file <testbed_file.yaml>
# Description: This job file checks that all BGP neighbors are in Established state
import os
from ats.easypy import run


# All run() must be inside a main function
def main():
    # Find the location of the script in relation to the job file
    bgp_tests = os.path.join('./BGP_Neighbors_Established.py')
    # Execute the testscript
    # run(testscript=testscript)
    run(testscript=bgp_tests)
