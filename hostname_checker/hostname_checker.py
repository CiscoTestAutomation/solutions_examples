# Simple Python script to verify if the hostname of the device is the
# same as the one in the yaml file. If not, change the device
# hostname for the yaml file one.
from genie.conf import Genie
from genie.libs import ops

testbed = "../default_testbed.yaml"

genie_testbed = Genie.init(testbed)

# Connect to each device in the yaml file
for dev in genie_testbed.devices.values():

    # Learn current hostname
    dev.connect(learn_hostname=True)
    # If hostname is not what is defined in the yaml file
    # Then change it
    if dev.hostname != dev.name:
        dev.hostname = dev.name
        dev.nodename = dev.name
        dev.state_machine.hostname = dev.name
        # Apply new hostname to the device
        dev.build_config()
