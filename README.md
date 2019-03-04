# pyATS and Genie Solutions examples

This repository contains several scripts for network health checking using the
[pyATS Framework](https://developer.cisco.com/site/pyats/)

These are intended be examples/starting points for solving common network operations
challenges.


# Installation / configuration

##### Installation
```
git clone https://github.com/CiscoTestAutomation/solutions_examples.git
cd solutions_examples
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

You can visit our [documentation](https://pubhub.devnetcloud.com/media/pyats-packages/docs/genie/cookbooks/genie.html#how-to-install-genie) for more information.

##### Simulation

We've provided a [topology.virl](./topology.virl) file for you to test with.

##### Testbed configuration

We've provided a [default_testbed.yaml](./testedbed.yaml) to go along with the
sample topology.  you'll likely need to change it to match your devices

# checks

* #### [bgp_adjacencies](./bgp_adjacencies) - "if a neighbor is configured, it should be established"

* #### [crc_errors](./crc_errors) - "No interface should be accumulating CRC errors"

* #### [hostname_checker](./hostname_checker) - "Verify devices hostname with Testbed file names"
