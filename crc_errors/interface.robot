# Execute a Test Case from Robot
# ================================================

*** Settings ***
Library        ats.robot.pyATSRobot

*** TestCases ***

Initialize
    # select the testbed to use
    use testbed "${testbed}"
    run testcase "CRC_Count_check.common_setup"


Check all interfaces for CRC errors
    run testcase "CRC_Count_check.CRC_count_check"
