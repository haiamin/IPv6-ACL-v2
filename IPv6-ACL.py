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
from netmiko import ConnectHandler
from datetime import datetime

# Define the names of files used
CSVDATA_FILENAME = 'devices.txt'
ACLDATA_FILENAME = 'acls.txt'

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
	# Fetch the current running configuration into output
    output = net_connect.send_command("show run")

    print "\n\n>>>>>>>>> Device {0} <<<<<<<<<".format(device['device_type'])


    for line in output.split('\n'):
        if "Giga" in line:
            print "##################### INTERFACE #####################"
     
        print "Line read: ", line
     
    print ">>>>>>>>> End <<<<<<<<<"
    net_connect.disconnect()

end_time = datetime.now()

total_time = end_time - start_time
print "Total time: ", total_time

