from napalm import get_network_driver
import os
import csv
import sys

devicetoconfigure = input(
    "Please enter the filename of the list of devices to be configured: "
)

if os.path.isfile(devicetoconfigure):
    print("Configuring devices found in " + devicetoconfigure)
else:
    print("File " + devicetoconfigure + " cannot be found.")
    sys.exit()

f = open(devicetoconfigure)
csv_f = csv.reader(f)

for row in csv_f:
    ios_family = row[0]
    ip = row[1]
    username = row[2]
    password = row[3]

    driver = get_network_driver(ios_family)
    device = driver(ip, username, password)
    device.open()
    facts = device.get_facts()
    print(facts["hostname"])

f.close()
