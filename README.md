[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/CiscoTestAutomation/solutions_examples)

# pyATS Solutions Examples

This repository contains several NetDevOps scripts build by our user community
using [pyATS Framework](https://developer.cisco.com/pyats/)

## Contributions

Everyone is welcome to leverage these scripts as starting points on solving 
common network operations challenges. 

If you have additional thoughts, ideas, or samples you'd like to contribute,
feel free to open a PR and become a member of the development community!

## Installation

```bash
# first, ensure you have a pyATS virtual environment
# eg:
mkdir -p ~/workspace/pyats
cd ~/workspace/pyats
python3 -m venv .
source bin/activate
pip install --upgrade pip setuptools
pip install pyats[full]

# now, clone this repository
git clone https://github.com/CiscoTestAutomation/solutions_examples
cd solutions_examples

# install the common dependencies
pip install -r requirements.txt

# you're good to go!
```

You can visit our [documentation](https://developer.cisco.com/docs/pyats/) for more information.

## VIRL Simulation

We've provided a [topology.virl](./topology.virl) file for you to test with.

## Testbed configuration

We've provided a [default_testbed.yaml](./testedbed.yaml) to go along with the
sample topology.  you'll likely need to change it to match your devices

## Notable Examples

* [bgp_adjacencies](./bgp_adjacencies) - "if a neighbor is configured, it should be established"

* [crc_errors](./crc_errors) - "No interface should be accumulating CRC errors"

* [hostname_checker](./hostname_checker) - "Verify devices hostname with Testbed file names"

