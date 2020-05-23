from napalm import get_network_driver
import csv

driver = get_network_driver("ios")
device = driver("192.168.1.1", "jays", "jayspalma")
device.open()
facts = device.get_facts()
print(facts["hostname"])

driver = get_network_driver("ios")
device = driver("192.168.1.2", "jays", "jayspalma")
device.open()
facts = device.get_facts()
print(facts["hostname"])


f = open("devices.csv")
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
