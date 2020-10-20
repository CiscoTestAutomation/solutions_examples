# From a single device point of view - how are other devices connected to it
# Provide a target-device - to learn how other devices are connected to it
# 1. Connect to all devices in the testbed file
# 2. Configure CDP on all these
# 3. Learn CDP neighbors and populate Excel sheet

# --target-device must be a device which exists in the testbed file. All
#                 devices which CDP must be configured must be provided
# --testbed-file   location of the testbed file

import re
import argparse
import xlsxwriter

from genie.testbed import load

# Provide argument at runtime
parser = argparse.ArgumentParser(description='')
parser.add_argument('--target-device',
                    type=str,
                    help='Central device to learn the connection')

parser.add_argument('--testbed-file',
                    type=str,
                    help='Testbed file')

# Get the device as an object
custom_args = parser.parse_known_args()[0]
local_device = custom_args.local_device
testbed_file = custom_args.testbed_file

# Make sure it exists
if not local_device:
    raise Exception('--local-device is a mandatory argument')

# Make sure it exists
if not testbed_file:
    raise Exception('--testbed-file is a mandatory argument')


# Load the testbed file
tb = load(testbed_file)

# Make sure the device exists
if local_device not in tb:
    raise Exception("'{}' does not exists in the testbed file".format(local_device))

# Store it as a variable
local_device = tb.devices[local_device]


# Connect to all the devices
tb.connect()

# Configure CDP for all the devices
for device in tb.devices.values():
    try:
        device.api.configure_cdp()
    except Exception as e:
        raise Exception('Could not configure CDP on {}\n'
                        '{}'.format(device.name, e))

# Learn the neighbors
try:
    output = local_device.api.get_cdp_neighbors_info()
except Exception as e:
    raise Exception('Could not learn cdp neighbor info on {}\n'
                    '{}'.format(local_device.name, e))

# Open up the excel to write to
workbook = xlsxwriter.Workbook('topology.xlsx')
worksheet = workbook.add_worksheet()

# Loop through each neighbors and check for
# Hostname
# Local Interface
# Remote Interface
# Remote Device
row = 0
for index, data in output['index'].items():
    # Get device name 
    remote_device_regex = re.compile(r'^.*?(?P<hostname>[-\w]+)\s?')

    # filter the host name from the domain name
    remote_device = data.get('system_name')
    if not remote_device:
        remote_device = data.get('device_id')

    regexed_name = remote_device_regex.match(remote_device)
    if not regexed_name:
        continue

    remote_device = regexed_name.groupdict()['hostname']

    # Verify this host is in the testbed file
    if remote_device not in tb.devices:
        #print("Device '{}' is not defined in the testbed "
        #      "file".format(remote_device))
        continue

    # Get Local and remote interface
    local_interface = data['local_interface']
    remote_interface = data['port_id']

    # Write to excel
    worksheet.write(row, 0, local_device.name)
    worksheet.write(row, 1, local_interface)
    worksheet.write(row, 2, remote_device)
    worksheet.write(row, 3, remote_interface)
    row += 1

workbook.close()
