#
# Title:	IPv6-ACL.py
# Author:	Niels Friis-Hansen
# Version:	1.0
#
# Revisions:	1.0	First draft version
#
# Descripion:
# Sample Python script that replaces ipv6 ACLs in Cisco IOS and ASA-type devices.
#
# The script logs into each device for which login credentials are provided in the "devices.txt" file,
# finds the defines ipv6 access-lists and delete each one, then adds new access-lists based on the contents of the file "acls.txt"
#
# The primary function of the script is to test Python functions and libraries.
#

import csv
import re
from netmiko import ConnectHandler
from datetime import datetime

# Define the names of files used
CSVDATA_FILENAME = 'devices.txt'
ACLDATA_FILENAME = 'acls.txt'

# Define list to hold config commands
config_cmds = []

# Record start-time
start_time = datetime.now()

# Define functions
def get_data(row):
	# Reads parameters from the CSV input-file
	data_fields = {
		field_name: field_value
		for field_name, field_value in row.items()
	}

# Main loop, log into each device for which credentials are included in the input CSV-file
for row in csv.DictReader(open(CSVDATA_FILENAME)):
    get_data(row)

	# Create a device object for input to netmikos ConnectHandler function
    device = {
        'device_type': row['DEVICETYPE'],
        'ip':   row['IP'],
        'username': row['USERNAME'],
        'password': row['PASSWORD'],
        'verbose': False,
    }

    # Connect to the device
    net_connect = ConnectHandler(**device)
	# ... and fetch the current running configuration into output
    output = net_connect.send_command("show run")

    # Read through the running config and look for lines starting with "ipv6 access-list "
    # If found, store the name of the access-list
    for line in output.split('\n'):
        matchObj = re.match( r'ipv6 access-list (.+)', line)
        if matchObj:
            print "Found ipv6 access-list", matchObj.group(1), "in", device['device_type'], "device with IP address", device['ip']
            # Now construct the IOS command required to remove the ACL
            cmd = "no ipv6 access-list " + matchObj.group(1)
            # And add command to list
            config_cmds.append(cmd)

    # Now, append the contents of ACLDATA_FILENAME to the config_commands list
    with open(ACLDATA_FILENAME, 'r') as f_acl:
        for line in f_acl:
            config_cmds.append(line.rstrip())
    f_acl.close()

    print "The following config-Commands will be sent to the device:"
    for c in config_cmds:
        print " ", c

    output = net_connect.send_config_set(config_cmds)
    output = net_connect.send_command("wr mem")
        
    net_connect.disconnect()

end_time = datetime.now()

total_time = end_time - start_time
print "Total run time: ", total_time

