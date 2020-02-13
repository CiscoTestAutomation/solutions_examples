# To run the job:
# pyats run job local_user_check_job.py --testbed-file <testbed_file.yaml> --local_users cisco admin
# Description: This job file checks for the existence of known local users
import os
import argparse
from pyats.datastructures.logic import Or


# All run() must be inside a main function
def main(runtime):
    parser = argparse.ArgumentParser()
    parser.add_argument('--local_users',
                        dest='expected_local_users',
                        nargs='+',
                        default=['cisco'])
    args, unknown = parser.parse_known_args()
    # Find the location of the script in relation to the job file
    local_user_check = os.path.join(os.path.dirname(__file__), 'local_user_check.py')
    # Execute the testscript
    runtime.tasks.run(testscript=local_user_check, 
                      taskid="Local User Check", 
                      **vars(args),
                      groups=Or('golden_config', 'bar'))
