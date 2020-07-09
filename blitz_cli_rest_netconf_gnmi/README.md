# Overview

This connects to your device via the following methods:
* Cli
* REST
* Netconf
* Gnmi

And execute 5 testcases:
* 4 testcases (one for each connection) will change the bgp neighbor 10.1.1.2 as-path, verify it changed, and change it back.
* 1 testcase will verify that the value for a specific key is the same across all 4 connections.

## Running

```
# run with your own device
pyats run genie --testbed-file testbed.yaml --mapping-datafile mapping_datafile.yaml --trigger-datafile trigger_datafile.yaml  --trigger-groups "And('all')"
```