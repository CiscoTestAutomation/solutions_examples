# Overview

This is a set of AeTest scripts which mainly make use of the Genie Tabular Parser for IOS-XR

The job file imports the custombits module which references a customize.yaml file.

The customize.yaml file can contain any AeTest scripts which you wish to execute instead of hard coding into the actual job file itself

Within customize.yaml is a list of PING targets showing that you add inputs into a YAML file and change them without touching the source code itself



# Running

```
pyats run job network_test_job.py --testbed-file <path to your IOSXR Testbed yaml file>


```
