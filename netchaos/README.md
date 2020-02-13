# netchaos

Proof of concept Network Chaos Monkey using Cisco VIRL, pyATS, and Genie

> Author: Kevin Corbin @kecorbin

# Configuration

you should only need to modify the [./mapping_datafile.yaml](./mapping_datafile.yaml) to
reflect the proper mappings to your `default_testbed.yaml` (**you must provide**) for details on creating one check [here](https://pubhub.devnetcloud.com/media/pyats/docs/topology/example.html)


# Let the chaos begin

```
make chaos
```

# Wait not so fast....

If you're scared - maybe start out with a single [Trigger](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/)

```
pyats run job network_chaos_monkey.py --testbed-file default_testbed.yaml --html-logs ./TriggerClearIpMroute.html --trigger TriggerClearIpMroute
```
