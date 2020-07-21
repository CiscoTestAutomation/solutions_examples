# Overview

This test job connects to all devices defined in the testbed, and pings a list of IP addresses.  The test passes if all ping succeed.

# Running

```
pyats run job ping_test_job.py --testbed-file ../default_testbed.yaml
```
