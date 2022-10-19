# pyATS dCloud examples

This folder have 3 examples for the following use cases:

## Pre / Post Checks

This example collects several commands for particular devices on a .xlsx sheet without fix testbed file and using threads to improve speed

Usage:

1_check_pyats.py [-h] --file FILE --type {pre,post} --credentials
                        CREDENTIALS [--jump JUMP]

Example:

$ python3 1_check_pyats.py --file device_info.xlsx --credentials cisco:cisco --type pre

## Collect and parse from devices

This example collects specific command, parses information and fills an output .xlsx sheet, again using threads

Usage:

2_collect_underlay.py [-h] --file FILE --credentials CREDENTIALS
                             [--jump JUMP]

Example:

$ python3 2_collect_underlay.py --file device_info.xlsx --credentials cisco:cisco 

## Audit using aetest framework

This example makes full audit for testbed on repo

Example:

$ pyats run job 3_job.py -t dCloud_local.yaml

## Walkthrough on dCloud Content Guide (in progress)
