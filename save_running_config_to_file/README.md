## Getting Started
1. Clone this repository into `<path/to/pyATS>/`

2. Create a [testbed datafile](https://pubhub.devnetcloud.com/media/pyats/docs/topology/schema.html#production-yaml-schema) 
that contains devices in which a backup is required.

3. Run the script which will, connect to all devices in the testbed datafile, gather the running configurations, 
and save that to a file named `<path/to/pyATS>/solutions_examples/save_running_config_to_file/config_backup_<dev_name>.txt`

        # Navigate to the cloned repository
        cd <path/to/pyATS>/solutions_examples/save_running_config_to_file
        
        # Execute the script
        pyats run job job.py --testbed-file <path/to/testbed.yaml>

4. If everything worked as expected the report at the end should be `PASSED` for every step:

        2020-09-03T10:25:21: %EASYPY-INFO: +------------------------------------------------------------------------------+
        2020-09-03T10:25:21: %EASYPY-INFO: |                             Task Result Details                              |
        2020-09-03T10:25:21: %EASYPY-INFO: +------------------------------------------------------------------------------+
        2020-09-03T10:25:21: %EASYPY-INFO: Task-1: genie_testscript
        2020-09-03T10:25:21: %EASYPY-INFO: |-- common_setup                                                          PASSED
        2020-09-03T10:25:21: %EASYPY-INFO: |   `-- connect                                                           PASSED
        2020-09-03T10:25:21: %EASYPY-INFO: |-- SaveDeviceConfigurationToFile.uut                                     PASSED
        2020-09-03T10:25:21: %EASYPY-INFO: |   `-- saving_config                                                     PASSED
        2020-09-03T10:25:21: %EASYPY-INFO: |       |-- STEP 1: Gathering the running configuration from all de...    PASSED
        2020-09-03T10:25:21: %EASYPY-INFO: |       `-- STEP 2: Saving all running configurations that were gat...    PASSED
        2020-09-03T10:25:21: %EASYPY-INFO: `-- common_cleanup                                                        PASSED
        2020-09-03T10:25:21: %EASYPY-INFO: Done!
        
5. View the logs by executing `pyats logs view`. The command will open a web browser where you can view the logs by section.


## What's Next
Now we have a text file containing a backup of the running configuration from all devices defined in the testbed datafile. 
One idea is using [pyATS Clean](https://pubhub.devnetcloud.com/media/genie-docs/docs/clean/index.html) 
to restore our configurations on a later date. This can be helpful if your network was working one day and not another. 
Simply replace to current configs with the backed up configs!

[pyATS Clean](https://pubhub.devnetcloud.com/media/genie-docs/docs/clean/index.html) has many other features worth looking into.
It can load new images onto various devices, recover devices from rommon prompt, and much much more.
