before:
	-easypy network_ops_profile.py -html_logs . -testbed_file ../default_testbed.yaml
	-open TaskLog.html
after:
	-easypy network_ops_profile.py -html_logs . -testbed_file ../default_testbed.yaml --after
	-open TaskLog.html

clean:
	-rm -rf runinfo archive
