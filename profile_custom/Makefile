before:
	-pyats run job network_ops_profile.py --html-logs. --testbed-file ../default_testbed.yaml
	-open TaskLog.html
after:
	-pyats run job network_ops_profile.py --html-logs. --testbed-file ../default_testbed.yaml --after
	-open TaskLog.html

clean:
	-rm -rf runinfo archive
