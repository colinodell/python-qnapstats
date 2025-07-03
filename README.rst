================
python-qnapstats
================

.. image:: https://img.shields.io/github/actions/workflow/status/colinodell/python-qnapstats/test.yml?branch=master&?style=flat-square
   :target: https://github.com/colinodell/python-qnapstats/actions?query=workflow%3ATest+branch%3Amaster
   :alt: Build Status
.. image:: https://img.shields.io/pypi/pyversions/qnapstats.svg?style=flat-square
   :target: https://pypi.python.org/pypi/qnapstats
   :alt: Supported Python Versions

Library from obtaining system information from QNAP NAS devices running QTS.

Installation
============

This library requires `xmltodict`, so make sure you have that installed:

.. code-block:: bash

    pip3 install xmltodict>=0.10.0

Then install this Python module:

.. code-block:: bash

    pip3 install qnapstats

Usage Example
=============

.. code-block:: python

    #!/usr/bin/env python3
    from qnapstats import QNAPStats
    from pprint import pprint
    
    qnap = QNAPStats('192.168.1.3', 8080, 'admin', 'correcthorsebatterystaple')
    
    pprint(qnap.get_system_stats())
    pprint(qnap.get_system_health())
    pprint(qnap.get_smart_disk_health())
    pprint(qnap.get_volumes())
    pprint(qnap.get_bandwidth())

Account
=======
The account you connect with must have system monitoring permissions. The simplest
option is to put it in the admin group; it doesn't necessarily
need to be THE "administrator" account, but you can use some account in the
administrators group.

Alternatively you can configure a normal account and enable Delegated Administration
in control panel, and activate "System Monitoring."

Once the account is created, and/or you upgrade to a newer of like QTS 5, 
also be sure to log into your NAS and complete any agreements, warnings, wizards, etc.
that may prevent this library from using the QNAP API.

MFA/2FA must also be disabled for that user for this library to work.

Device Support
==============

This library has been tested against the following devices and firmwares:

+--------------+------------------------+---------------------------------------+
| Model        | QTS* Firmware Versions | Notes                                 |
+==============+========================+=======================================+
| D4 Pro       | 4.5.1                  | User-reported: no automated tests     |
+--------------+------------------------+---------------------------------------+
| TS-110       | 4.2.4                  |                                       |
+--------------+------------------------+---------------------------------------+
| TS-112P      | 4.3.3                  | This device does not report CPU temps |
+--------------+------------------------+---------------------------------------+
| TS-210       | 4.2.6                  | This device does not report CPU temps |
+--------------+------------------------+---------------------------------------+
| TS-219P II   | 4.3.3                  | User-reported: no automated tests     |
+--------------+------------------------+---------------------------------------+
| TS-251B      | 4.4.3                  |                                       |
+--------------+------------------------+---------------------------------------+
| TS-228A      | 5.0.1                  | This device does not report CPU temps |
+--------------+------------------------+---------------------------------------+
| TS-233       | 5.1.x                  |                                       |
+--------------+------------------------+---------------------------------------+
| TS-251+      | 4.5.1                  | No information on dnsInfo             |
+--------------+------------------------+---------------------------------------+
| TS-253 Pro   | 4.5.2                  |                                       |
+--------------+------------------------+---------------------------------------+
| TS-253D      | 4.5.3                  |                                       |
+--------------+------------------------+---------------------------------------+
| TS-332       | 5.0.0                  |                                       |
+--------------+------------------------+---------------------------------------+
| TS-364       | 5.0.1                  |                                       |
+--------------+------------------------+---------------------------------------+
| TS-269L      | 4.3.3                  | User-reported: no automated tests     |
+--------------+------------------------+---------------------------------------+
| TS-410       | 4.2.3                  | This device does not report CPU temps |
+--------------+------------------------+---------------------------------------+
| TS-412       | 4.3.3                  | This device does not report CPU temps |
+--------------+------------------------+---------------------------------------+
| TS-431P      | 4.3.4                  |                                       |
+--------------+------------------------+---------------------------------------+
| TS-451       | 4.2.2 - 4.2.4          |                                       |
+--------------+------------------------+---------------------------------------+
| TS-453A      | 4.3.4; 5.0.1           |                                       |
+--------------+------------------------+---------------------------------------+
| TS-453Be     | 4.2.3; 5.0.1           |                                       |
+--------------+------------------------+---------------------------------------+
| TS-464       | 5.2.5                  | User-reported: no automated tests     |
+--------------+------------------------+---------------------------------------+
| TS-639       | 4.2.3                  |                                       |
+--------------+------------------------+---------------------------------------+
| TS-659       | 4.2.6                  | May report `None` for some disk temps |
+--------------+------------------------+---------------------------------------+
| TS-853 Pro   | 4.5.4                  |                                       |
+--------------+------------------------+---------------------------------------+
| TS-869 Pro   | 4.3.4                  |                                       |
+--------------+------------------------+---------------------------------------+
| TS-873A      | 5.0.1.2248             |                                       |
+--------------+------------------------+---------------------------------------+
| TS-1677XU-RP | 4.5.2                  |                                       |
+--------------+------------------------+---------------------------------------+
| TS-EC1280U   | 4.5.2                  |                                       |
+--------------+------------------------+---------------------------------------+
| TS-h886      | QuTS h5.0.1.2376       |                                       |
+--------------+------------------------+---------------------------------------+
| TS-X53       | 4.5.4                  |                                       |
+--------------+------------------------+---------------------------------------+
| TVS-672N     | 5.0.1                  |                                       |
+--------------+------------------------+---------------------------------------+
| TVS-1282     | 5.0.1                  |                                       |
+--------------+------------------------+---------------------------------------+

⚠️ *QuTS is not currently supported - see [issue #84](https://github.com/colinodell/python-qnapstats/issues/84)*

Other QNAP devices using these QTS firmwares should probably work fine, as should the devices listed above on newer firmwares.
If you encounter any compatibility issues, please let us know (or better yet, contribute a patch!)


**Upgrading to QTS 5?** Make sure the account you connect with meets the criteria listed earlier in this README.
Also be sure to log into your NAS and complete any agreements, warnings, wizards, etc. that may prevent this
library from using the QNAP API.
