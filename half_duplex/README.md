# Overview

This test job connects to all devices defined in the testbed, and searches for interfaces working in half duplex mode.  The test passes if all `physical` interfaces found `active` are in `full duplex` state.

# Running

```
pyats run job half_duplex_job.py --testbed-file ../default_testbed.yaml
```
