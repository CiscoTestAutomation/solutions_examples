# Overview

This check connects to all devices defined in the testbed, and parses locally configured
usernames against a list provided at runtime, the test passes if all usernames (an no additional)
users are configured on the device.

# Running

```
pyats run job local_user_check_job.py --html-logs--testbed-file ../default_testbed.yaml --local_users cisco admin
```
