# Shut all un-used interface, where the out_pkts is 0.
# Example testbed file provided

from genie.testbed import load
tb = load('testbed.yaml')
dev = tb.devices['csr1000v-1']
dev.connect()
x = dev.parse('show interfaces')

for interface, interface_data in x.items():
    if 'counters' in interface_data:
       if 'out_pkts' in interface_data['counters']:
           if x[interface]['counters']['out_pkts'] == 0 :
                dev.configure('int {}\n shutdown'.format(interface))
