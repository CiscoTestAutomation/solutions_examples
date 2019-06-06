# netchaos

Proof of concept Network Chaos Monkey using Cisco VIRL, pyATS, and Genie

> Author: Kevin Corbin @kecorbin

# Requirements

pyATS requires python3 make sure you've installed the requirements in your virtualenv

```
pip install -r requirements.txt
```

# Configuration

you should only need to modify the [./mapping_datafile.yaml](./mapping_datafile.yaml) to
reflect the proper mappings to your `default_testbed.yaml` (**you must provide**) for details on creating one check [here](https://pubhub.devnetcloud.com/media/pyats/docs/topology/example.html)


# Let the chaos begin

```
make chaos
```

# Wait not so fast....

If you're scared - maybe start out with a single [Trigger](https://pubhub.devnetcloud.com/media/pyats-packages/docs/genie/genie_libs/#/triggers)

```
pyats run job network_chaos_monkey.py --testbed-file default_testbed.yaml --html-logs ./TriggerClearIpMroute.html --trigger TriggerClearIpMroute
```
