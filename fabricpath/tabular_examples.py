from genie.conf import Genie
from genie import parsergen
from genie.utils.diff import Diff
from pprint import pprint


# Create Testbed Object with Genie
testbed = Genie.init('../default_testbed.yaml')

# Create Device Object
uut = testbed.devices['uut']

# Use connect method to initiate connection to the device under test
uut.connect()

# Execute command show nve nvi on connected device

# Create list of Header names of the table from the show_command
# these must match exactly to that which is output on cli
header = ['System ID', 'SNPA', 'Level', 'State', 'Hold Time', 'Interface']

# Capture Before output
before = uut.device.execute('show fabricpath isis adjacency')
before = parsergen.oper_fill_tabular(device_output=before,
                                     device_os='nxos',
                                     header_fields=header,
                                     index=[0])

# Capture after output
after = uut.device.execute('show fabricpath isis adjacency')
after = parsergen.oper_fill_tabular(device_output=after,
                                    device_os='nxos',
                                    header_fields=header,
                                    index=[0])

pprint(after.entries)
exclude = ['Hold Time']
dd = Diff(before.entries, after.entries, exclude=exclude)
dd.findDiff()
print(dd)

command = "show fabricpath switch-id"
output = uut.device.execute(command)
header_fields = ['SWITCH-ID', '   SYSTEM-ID', ' FLAGS',
                 '   STATE', '  STATIC', '  EMULATED/']
label_fields = ['SWITCH-ID', 'SYSTEM-ID', 'FLAGS',
                'STATE', 'STATIC', 'EMULATED/ANYCAST']
topology = parsergen.oper_fill_tabular(device_output=output,
                                       header_fields=header_fields,
                                       label_fields=label_fields,
                                       index=[1])
pprint(topology.entries)


# show fabricpath isis interface brief
command = 'show fabricpath isis interface brief'
header = ['Interface', 'Type', 'Idx', 'State', 'Circuit',
          'MTU', 'Metric', 'Priority', 'Adjs/AdjsUp']
int_brief = parsergen.oper_fill_tabular(device=uut,
                                        show_command=command,
                                        header_fields=header,
                                        index=[0])
pprint(int_brief.entries)


# sh fabricpath isis host
command = "sh fabricpath isis host"
output = uut.device.execute(command)
header = ['Level', 'System ID', 'Dynamic hostname']
label_fields = ['level', 'system_id', 'hostname']
isis_hosts = parsergen.oper_fill_tabular(device_output=output,
                                         device_os='nxos',
                                         header_fields=header,
                                         label_fields=label_fields,
                                         index=[1])
pprint(isis_hosts.entries)
