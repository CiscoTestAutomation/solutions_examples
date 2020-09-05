import logging

from genie.harness.base import Trigger
from pyats import aetest
from pyats.async_ import pcall

log = logging.getLogger(__name__)

class SaveDeviceConfigurationToFile(Trigger):
    """ Trigger to save the running configuration of a device to a file """

    @aetest.test
    def saving_config(self, steps, testbed, exclude_config_that_matches_regex):
        with steps.start("Gathering the running configuration from all "
                         "devices in the testbed file") as step:

            # Get all devices in the testbed
            devices = list(testbed.devices.values())

            try:
                # Use pcall to get configuration from all devices in parallel
                configurations = pcall(
                    self.get_config,
                    dev=devices,
                    ckwargs={'exclude': exclude_config_that_matches_regex}
                )
            except Exception as e:
                step.failed("Issue occurred while gathering running "
                            "configuration.\nError: {}".format(str(e)))

            step.passed("Gathered the running configuration for: {}".format(
                [name for name, config in configurations if isinstance(config, str)]))

        with steps.start("Saving all running configurations that were "
                         "gathered"):

            for dev, config in configurations:

                # Skip any devices where the api to gather the running
                # config does not exist
                if isinstance(config, AttributeError):
                    log.warning(config)
                    continue

                filename = 'config_backup_{}.txt'.format(dev)

                with open(filename, 'w') as f:
                    f.write(config)

                log.info("Saved '{dev}' running configuration to '{file}'"
                         .format(dev=dev, file=filename))

    @staticmethod
    def get_config(dev, exclude):
        """ Returns a valid configuration from a device

            Args:
                dev ('obj'): Device to get configuration from
                exclude ('str'): A regex that is used to exclude any lines
                                 that match from the returned configuration

            Returns:
                (device name ('str'), configuration ('str'))

                if api not found:
                (device name ('str'), exception ('exception'))
        """

        exclude = exclude.get(dev.os)

        log.info("The following regex is used to exclude lines of "
                 "configuration for '{}' devices: {}"
                 .format(dev.os, exclude))
        try:
            out = dev.api.get_valid_config_from_running_config(exclude=exclude)
        except AttributeError:
            return dev.name, AttributeError("Cannot get the config from '{}'. "
                                            "The API is not developed for '{}'"
                                            .format(dev.name, dev.os))

        return dev.name, out