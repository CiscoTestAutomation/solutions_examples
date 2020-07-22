"""
half_duplex_job.py

"""
# see https://pubhub.devnetcloud.com/media/pyats/docs/easypy/jobfile.html
# for how job files work

__author__ = "Oren Brigg"
__copyright__ = "Copyright (c) 2020, Cisco Systems Inc."
__contact__ = ["obrigg@cisco.com"]
__credits__ = ["hapresto@cisco.com"]
__version__ = 1.0

import os
from pyats.easypy import run

# compute the script path from this location
SCRIPT_PATH = os.path.dirname(__file__)


def main(runtime):
    """job file entrypoint"""

    # run script
    run(
        testscript=os.path.join(SCRIPT_PATH, "testbed_connection.py"),
        runtime=runtime,
        taskid="Device Connections",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "half_duplex.py"),
        runtime=runtime,
        taskid="Half Duplex",
    )
