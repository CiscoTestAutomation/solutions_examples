"""
network_test_job.py

Using the customize.yaml file
we will read in all the scripts

custombits module is used to read in the yaml file
and execute the scripts instead of hardcoding directly

"""

import os
from pyats.easypy import run
from custombits import CustomBits

# compute the script path from this location
SCRIPT_PATH = os.path.dirname(__file__)

def main(runtime):
    """job file entrypoint"""

    # run script
    job_dict = CustomBits().joblist()
    for script in job_dict:
        name = job_dict[script]['name']
        taskid = job_dict[script]['taskid']
        run(
            testscript=os.path.join(SCRIPT_PATH, name),
            runtime=runtime,
            taskid=taskid,
        )
 
