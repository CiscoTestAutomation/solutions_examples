# Take initial snapshot of the operational state of the device
# and save the output to a file

*** Settings ***
# Importing test libraries, resource files and variable files.
Library        ats.robot.pyATSRobot
Library        genie.libs.robot.GenieRobot


*** Variables ***
# Define the pyATS testbed file to use for this run
#${testbed}     /root/katacoda-scenarios/compare/tb.yaml
${testbed}     ../default_testbed.yaml

*** Test Cases ***
# Creating test cases from available keywords.

Connect
    # Initializes the pyATS/Genie Testbed
    use genie testbed "${testbed}"

    # Connect to both device
    connect to device "spine1"
    connect to device "leaf1"

Profile the devices
    Profile the system for "bgp;config;interface;platform;ospf;arp;routing;vrf;vlan" on devices "leaf1" as "./good_snapshot"
