from napalm import get_network_driver

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
