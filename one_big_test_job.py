# To run the job:
# pyats run job one_big_test_job.py --testbed-file <testbed_file.yaml> --local_users cisco admin

# Description: This job file runs multiple testcases from different files
# there are various ways and reasons to do so depending on use case

# For more information refer to the documentation here:
# https://pubhub.devnetcloud.com/media/pyats/docs/easypy/jobfile.html#

import os
import argparse

HERE = os.path.dirname(__name__)

# All run() must be inside a main function
def main(runtime):
    parser = argparse.ArgumentParser()
    parser.add_argument('--local_users',
                        dest='expected_local_users',
                        nargs='+',
                        default=['cisco'])
    args, unknown = parser.parse_known_args()
    # Find the location of the script in relation to the job file
    local_user_check = os.path.join(HERE, 'local_users', 'local_user_check.py')
    # Execute the testscript as task
    task_1 = runtime.tasks.Task(testscript=local_user_check,
                                runtime=runtime,
                                taskid='Validate Locally Configured Usernames',
                                 **vars(args))
    task_1.start()
    # wait for a max runtime of 60*5 seconds = 5 minutes
    task_1.wait(60*5)

    # add another task
    bgp_neighbors_check = os.path.join(HERE, 'bgp_adjacencies', 
                                       'BGP_Neighbors_Established.py')
    task_2 = runtime.tasks.Task(testscript=bgp_neighbors_check,
                                runtime=runtime,
                                taskid='Verify BGP neighbors are established',
                                **vars(args))

    task_2.start()
    task_2.wait(60*5)

    crc_check = os.path.join(HERE, 'crc_errors', 'script.py')

    # or simply call run as many times as you'd like
    runtime.tasks.run(testscript=crc_check, 
                      taskid="Check all Interfaces for CRC errors", 
                        **vars(args))
