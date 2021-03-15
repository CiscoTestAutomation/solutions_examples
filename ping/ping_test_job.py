# see https://pubhub.devnetcloud.com/media/pyats/docs/easypy/jobfile.html
# for how job files work

__author__ = "Oren Brigg"
__copyright__ = "Copyright (c) 2020, Cisco Systems Inc."
__contact__ = ["obrigg@cisco.com"]
__credits__ = ["hapresto@cisco.com"]
__version__ = 1.0

import os
import argparse
from pyats.easypy import run

# command line argument parser
# see https://pubhub.devnetcloud.com/media/pyats/docs/easypy/jobfile.html#custom-arguments
parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dest",
        dest = "ping_list",
        type=str,
        default = "208.67.222.222 8.8.8.8 1.1.1.1",
        help = "space delimted list of IP address(es) to test connectivity"
    )
# compute the script path from this location
SCRIPT_PATH = os.path.dirname(__file__)

def main(runtime):
    """job file entrypoint"""
    # parse command line arguments
    # only parse arguments we know
    args, _ = parser.parse_known_args()

    # run script, pass arguments to script as parameters
    run(
        testscript=os.path.join(SCRIPT_PATH, "ping_test.py"),
        runtime=runtime,
        taskid="Ping",
        **vars(args)
    )
