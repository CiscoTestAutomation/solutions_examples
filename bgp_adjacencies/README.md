# Overview

This check connects to all devices defined in the testbed, and parses BGP operational data.  The test passes if all BGP neighbors found are in the `established` state. 

# Running

```
easypy BGP_check_job.py -html_logs -testbed_file ../default_testbed.yaml
```
