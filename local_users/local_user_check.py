#!/bin/env python
import logging
from pyats import aetest
from pyats.log.utils import banner
from genie.conf import Genie
from genie.libs import ops # noqa

log = logging.getLogger(__name__)


class common_setup(aetest.CommonSetup):
    """ Common Setup section """

    # Connect to each device in the testbed
    @aetest.subsection
    def connect(self, testbed):
        genie_testbed = Genie.init(testbed)
        self.parent.parameters['testbed'] = genie_testbed
        device_list = []
        for d in genie_testbed.devices.keys():
            # Mark testcase with looping information
            device = genie_testbed.devices[d]

            log.info(banner(
                "Connect to device '{d}'".format(d=device.name)))
            try:
                device.connect()
                device_list.append(d)

            except Exception as e:
                msg = "Failed to connect to {} will not be checked!"
                log.info(msg.format(device.name))

        # run local_user_check against each device in the list
        aetest.loop.mark(local_user_check, dev_name=device_list)


class local_user_check(aetest.Testcase):

    groups = ['aaa', 'golden_config']

    @aetest.test
    def compare_local_users(self, steps, dev_name, expected_local_users):
        """Local User Database checks

        Given a list of expected usernames validates they
        are present on the device

        """
        device = self.parent.parameters['testbed'].devices[dev_name]
        with steps.start('Getting Configured Usernames'):
            usernames = device.execute('show run | inc username')
            lines = usernames.split('\r\n')
            cfg_local_users = [w.split(' ')[1] for w in lines]
            log.info('Configured Users: {}'.format(cfg_local_users))

        with steps.start('Comparing Configured Usernames'):
            msg = 'Checking for {} in local user database'
            log.info(msg.format(expected_local_users))
            if not sorted(expected_local_users) == sorted(cfg_local_users):
                self.failed("User lists are not same")


if __name__ == '__main__':  # pragma: no cover
    aetest.main()
