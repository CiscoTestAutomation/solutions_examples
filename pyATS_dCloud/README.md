# pyATS dCloud examples

This folder have 3 examples for the following use cases:

## Pre / Post Checks

This example collects several commands for particular devices on a .xlsx sheet

Usage:

1_check_pyats.py [-h] --file FILE --type {pre,post} --credentials
                        CREDENTIALS [--jump JUMP]

Example:

$ python3 1_check_pyats.py --file device_info.xlsx --credentials cisco:cisco --type {pre,post}

