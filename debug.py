#!/usr/bin/env python3
import getpass
import traceback
import qnapstats

host = input("Host (prefix with 'https://' if needed): ")
port = int(input("Port: "))
username = input("Username: ")
password = getpass.getpass("Password: ")

qnap = qnapstats.QNAPStats(host, port, username, password, debugmode=True, verify_ssl=False)

try:
    qnap.get_system_stats()
except Exception as e:
    print(e.args)
    traceback.print_exc()

try:
    qnap.get_system_health()
except Exception as e:
    print(e.args)
    traceback.print_exc()

try:
    qnap.get_smart_disk_health()
except Exception as e:
    print(e.args)
    traceback.print_exc()

try:
    qnap.get_volumes()
except Exception as e:
    print(e.args)
    traceback.print_exc()

try:
    qnap.get_bandwidth()
except Exception as e:
    print(e.args)
    traceback.print_exc()

try:
    qnap.get_storage_information_on_external_device()
except Exception as e:
    print(e.args)
    traceback.print_exc()
