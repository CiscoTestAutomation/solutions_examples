# Take initial snapshot of the operational state of the device
# and save the output to a file

*** Settings ***
# Importing test libraries, resource files and variable files.
Library        ats.robot.pyATSRobot
Library        genie.libs.robot.GenieRobot


*** Variables ***
# Define the pyATS testbed file to use for this run
#${testbed}     /root/katacoda-scenarios/robot/tb.yaml 
${testbed}     tb.yaml 

*** Test Cases ***
# Creating test cases from available keywords.

Connect
    # Initializes the pyATS/Genie Testbed
    use genie testbed "${testbed}"

    # Connect to both device
    connect to device "nx-osv-1"
    connect to device "csr1000v-1"

Profile bgp & ospf on uut
    Profile the system for "bgp;config;interface;platform;ospf" on devices "nx-osv-1;csr1000v-1" as "./second_snapshot"

Compare snapshots
    Compare profile "./initial_snapshot" with "./second_snapshot" on devices "nx-osv-1;csr1000v-1"
