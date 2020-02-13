'''
To run the job:

$ pyats run job job.py --testbed-file <testbed_file.yaml>

Additional CLI Arguments:
    --no-parallel-connect: disables parallel device connection
    --crc-threshold: max crc interface error before it's called to be a failure

Example:
$ pyats run job job.py --testbed-file ../devnet_sandbox.yaml --crc-threshold 100 --no-parallel-connect
'''

import os
import argparse

# command line argument parser
# see https://pubhub.devnetcloud.com/media/pyats/docs/easypy/jobfile.html#custom-arguments
parser = argparse.ArgumentParser()
parser.add_argument('--no-parallel-connect',
                    dest = 'p_connect',
                    action='store_false',
                    default = True,
                    help = 'disable connecting to devices in parallel')
parser.add_argument('--crc-threshold',
                    dest = 'crc_threshold',
                    default = 0,
                    type = int,
                    help = 'threshold at which interface CRC will be considered'
                           'fail')

def main(runtime):
    # parse command line arguments
    # only parse arguments we know
    args, _ = parser.parse_known_args()

    # Find the location of the script in relation to the job file
    testscript = os.path.join(os.path.dirname(__file__), 'script.py')
    
    # run script, pass arguments to script as parameters
    runtime.tasks.run(testscript=testscript,
                      **vars(args))
