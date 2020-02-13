# Overview

This check connects to all devices defined in the testbed, and parses are interface counters
if an interface has CRC errors, the test case fails. 

## Running

```
# run with the provided devnet always-on sandbox
pyats run job job.py --testbed-file ../default_testbed.yaml

# run with the provided mock devices (does not require real testbed)
pyats run job job.py --testbed-file ../default_testbed.yaml  --replay mock
```