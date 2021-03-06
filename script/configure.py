from napalm import get_network_driver
from netmiko.ssh_exception import NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
import os
import csv
import sys
import logging
from datetime import datetime


logging.basicConfig(filename="error.log", level=logging.ERROR, filemode="w")

devicetoconfigure = input(
    "Please enter the filename of the list of devices to be configured: "
)

if os.path.isfile(devicetoconfigure):
    pass
else:
    while not os.path.isfile(devicetoconfigure):
        devicetoconfigure = input(
            "Please check the if filename is correct or type the aboslute path to the file or type 'exit' to quit. "
        )

        if (devicetoconfigure).lower() == "exit":
            print("Exiting...")
            sys.exit()
        else:
            os.path.isfile(devicetoconfigure)

print("Configuring devices found in " + devicetoconfigure)

f = open(devicetoconfigure)
csv_f = csv.reader(f)

for row in csv_f:
    ios_family = row[0]
    ip = row[1]
    username = row[2]
    password = row[3]
    config = row[4]

    driver = get_network_driver(ios_family)
    device = driver(ip, username, password)
    try:
        print("Configuring " + ip + "...", end="")
        device.open()

    except NetmikoAuthenticationException:
        print("Failed!")
        logging.error(
            str(datetime.now())
            + " Error cofiguring "
            + ip
            + " :"
            + " Wrong use/password."
        )
        continue

    except SSHException:
        print("Failed!")
        logging.error(
            str(datetime.now())
            + " Error cofiguring "
            + ip
            + " :"
            + " SSH not enabled on device."
        )
        continue

    except Exception:
        print("Failed!")
        logging.error(
            str(datetime.now())
            + " Error cofiguring "
            + ip
            + " :"
            + " Unknown error: Check the device SSH configuration"
        )
        continue

    try:
        device.load_merge_candidate(config)
        print("Success!")
        device.commit_config()
    except FileNotFoundError:
        print("Failed!")
        logging.error(
            str(datetime.now())
            + " Error cofiguring "
            + ip
            + " :"
            + " Configuration file cannot be found"
        )
        continue


f.close()
