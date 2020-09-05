## Important Information
Minimum version requirements:

    - v20.8 pyATS
    - v20.8 Genie
    - v20.8.3b0 genie.libs.sdk
    - v20.8.2b2 genie.libs.clean
    
If the versions of your packages do not meet the above minimums, upgrade using the steps below:

    # First upgrade the pyats installation to 20.8
    pip install --upgrade pyats[full]
    
    # Next upgrade genie.libs.sdk and genie.libs.clean to the beta
    pip install --upgrade --pre genie.libs.sdk genie.libs.clean


## Getting Started
1. Clone this repository into `<path/to/pyATS>/`

2. Create a [testbed datafile](https://pubhub.devnetcloud.com/media/pyats/docs/topology/schema.html#production-yaml-schema) 
that contains devices in which a backup is required. 

    **note:** One device must have the alias 'uut' (does not matter which one).

3. Run the script which will, connect to all devices in the testbed datafile, gather the running configurations, 
and save that to a file named `<path/to/pyATS>/solutions_examples/save_running_config_to_file/config_backup_<dev_name>.txt`

        # Navigate to the cloned repository
        cd <path/to/pyATS>/solutions_examples/save_running_config_to_file
        
        # Execute the script
        pyats run job job.py --testbed-file <path/to/testbed.yaml>
        
    **note**: For this example only ios, iosxe, iosxr, and nxos device are supported. Any other devices will be skipped.

4. If everything worked as expected, the report at the end should be `PASSED` for every step:

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
Simply replace the current configs with the backed up configs!

1. Edit the `clean.yaml` template provided in `<path/to/pyATS>/solutions_examples/save_running_config_to_file/datafiles` 
to include your devices and the path to the config_backup_<dev_name>.txt file. You can add as many devices that are in your testbed file.

2. Run clean to restore your configs.
    
        # Navigate to cloned repository
        cd <path/to/pyATS>/solutions_examples/save_running_config_to_file
        
        # Run clean
        kleenex -testbed_file <path/to/testbed.yaml> -clean_file datafiles/clean.yaml
        
3. If everything worked successfully the report at the end should be `Passed` for every step:

        2020-09-05T08:18:10: %AETEST-INFO: +----------------------------------------------------------+
        2020-09-05T08:18:10: %AETEST-INFO: |                       STEPS Report                       |
        2020-09-05T08:18:10: %AETEST-INFO: +----------------------------------------------------------+
        2020-09-05T08:18:10: %AETEST-INFO: STEP 1 - Apply configuration to device <dev> after reload    Passed
        2020-09-05T08:18:10: %AETEST-INFO: STEP 2 - Copy running-config to startup-config on device <dev>    Passed
        2020-09-05T08:18:10: %AETEST-INFO: STEP 3 - Allow configuration to stabilize on device <dev>    Passed
        2020-09-05T08:18:10: %AETEST-INFO: ------------------------------------------------------------
        2020-09-05T08:18:10: %AETEST-INFO: The result of section apply_configuration is => PASSED
        2020-09-05T08:18:10: %KLEENEX-INFO: Finished cleaning device '<dev>' using 'DeviceClean'.
        2020-09-05T08:18:11: %ROOT-INFO: Clean finished!

[pyATS Clean](https://pubhub.devnetcloud.com/media/genie-docs/docs/clean/index.html) has many other features worth looking into.
It can load new images onto various devices, recover devices from rommon prompt, and much much more.
