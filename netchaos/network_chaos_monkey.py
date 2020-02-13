import os
from pyats.datastructures.logic import And, Not, Or
from genie.harness.main import gRun
import argparse

# chaos only knows..
import random

# how brave are you?
# comprehensive list of triggers / docs located at
# https://pubhub.devnetcloud.com/media/pyats-packages/docs/genie/genie_libs/#/triggers

POSSIBLE_TRIGGERS = [
    'TriggerClearBgpAll',
    'TriggerClearIpOspfNeighborVrfAll',
    'TriggerClearIpRoute',
    'TriggerUnconfigConfigEvpnVni',
    'TriggerUnconfigConfigVlanInterface',
    'TriggerUnconfigConfigVlanVnsegment',
    # 'TriggerClearIpMroute'

]

RANDOM_TRIGGER = random.choice(POSSIBLE_TRIGGERS)


""" KNOWN_ISSUES """


"""
'TriggerUnconfigConfigNvOverlayEvpn'


'TriggerUnconfigConfigBgp'

2019-01-16T22:55:58: %AETEST-ERROR: Failed reason: Failed to unconfigure feature
2019-01-16T22:55:58: %AETEST-ERROR:
2019-01-16T22:55:58: %AETEST-ERROR: Exception:
2019-01-16T22:55:58: %AETEST-ERROR: Traceback (most recent call last):
2019-01-16T22:55:58: %AETEST-ERROR:   File "/Users/kecorbin/VirtualEnvs/netchaos/lib/python3.6/site-packages/genie/libs/sdk/triggers/unconfigconfig/unconfigconfig.py", line 100, in unconfigure
2019-01-16T22:55:58: %AETEST-ERROR:     self.mapping.unconfigure(device=uut, abstract=abstract, steps=steps)
2019-01-16T22:55:58: %AETEST-ERROR:   File "/Users/kecorbin/VirtualEnvs/netchaos/lib/python3.6/site-packages/genie/libs/sdk/libs/utils/mapping.py", line 1071, in unconfigure
2019-01-16T22:55:58: %AETEST-ERROR:     return self.configure(unconfig=True, *args, **kwargs)
2019-01-16T22:55:58: %AETEST-ERROR:   File "/Users/kecorbin/VirtualEnvs/netchaos/lib/python3.6/site-packages/genie/libs/sdk/libs/utils/mapping.py", line 1156, in configure
2019-01-16T22:55:58: %AETEST-ERROR:     unconfig, name, **kwarg)
2019-01-16T22:55:58: %AETEST-ERROR:   File "/Users/kecorbin/VirtualEnvs/netchaos/lib/python3.6/site-packages/genie/libs/sdk/libs/utils/mapping.py", line 1163, in _configure
2019-01-16T22:55:58: %AETEST-ERROR:     co = abstracted_ops(device=device, **kwargs)
2019-01-16T22:55:58: %AETEST-ERROR:   File "/Users/kecorbin/VirtualEnvs/netchaos/lib/python3.6/site-packages/genie/libs/conf/bgp/bgp.py", line 1288, in __init__
2019-01-16T22:55:58: %AETEST-ERROR:     self.bgp_id = int(bgp_id)
2019-01-16T22:55:58: %AETEST-ERROR: TypeError: int() argument must be a string, a bytes-like object or a number, not 'list'

"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--trigger',
                        dest='trigger',
                        default=None)
    # parser.add_argument('--inventory',
    #                     dest='inventory',
    #                     default='inventory/test.yaml')
    args, unknown = parser.parse_known_args()

    test_path = os.path.dirname(os.path.abspath(__file__))
    # print(args)

    # mapping_datafile is mandatory
    # trigger_uids limit which test to execute

    if args.trigger:
        trigger = args.trigger
    else:
        trigger = RANDOM_TRIGGER


    gRun(mapping_datafile=os.path.join(test_path, 'mapping_datafile.yaml'),
         pts_datafile='pts_datafile.yaml',
         pts_features=['ospf', 'bgp'],
         trigger_uids=Or(trigger))
