# Overview

This test job connects to all devices defined in the testbed, and searches for differences between the `running config` and the `startup config`.  The test passes if all `running configs` and `startup configs` are in sync.

# Running

```
pyats run job run_vs_start_job.py --testbed-file ../default_testbed.yaml
```
