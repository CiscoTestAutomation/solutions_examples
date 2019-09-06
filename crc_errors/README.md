# Overview

This check connects to all devices defined in the testbed, and parses are interface counters
if an interface has CRC errors, the test case fails. 

# Running

```
pyats run job CRC_check_job.py -html_logs -testbed_file ../default_testbed.yaml
```


# To use the Mock device
pyats run job CRC_check_job.py -html_logs -testbed_file ../default_testbed.yaml  --replay mock
