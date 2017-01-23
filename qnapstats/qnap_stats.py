"""Module containing multiple classes to obtain QNAP system stats via cgi calls."""
# -*- coding:utf-8 -*-
from lxml import etree
import requests

TIMEOUT = 5


class QNAPStats(object):
    """Class containing the main functions."""

    def __init__(self, host, port, username, password, debugmode=False):
        """Instantiate a new qnap_stats object."""
        import base64
        self._username = username
        self._password = base64.b64encode(password.encode('utf-8')).decode('ascii')

        self._sid = None
        self._debugmode = debugmode

        self._session_error = False
        self._session = None  # type: requests.Session

        if not host.startswith("http://") or host.startswith("https://"):
            host = "http://" + host

        self._base_url = '%s:%s/cgi-bin/' % (host, port)

    def _debuglog(self, message):
        """Output message if debug mode is enabled."""
        if self._debugmode:
            print("DEBUG: " + message)

    def _init_session(self):
        if self._sid is None or self._session is None or self._session_error:
            # Clear sid and reset error
            self._sid = None
            self._session_error = False

            if self._session is not None:
                self._session = None
            self._debuglog("Creating new session")
            self._session = requests.Session()

            # We created a new session so login
            if self._login() is False:
                self._session_error = True
                self._debuglog("Login failed, unable to process request")
                return

    def _login(self):
        """Log into QNAP and obtain a session id."""
        data = {"user": self._username, "pwd": self._password}
        result = self._execute_post_url("authLogin.cgi", data, False)

        if result is None:
            return False

        self._sid = result.xpath("authSid")[0].text.strip()
        return True

    def _get_url(self, url, retry_on_error=True):
        """High-level function for making GET requests."""
        self._init_session()

        result = self._execute_get_url(url)
        if (self._session_error or result is None) and retry_on_error:
            self._debuglog("Error occured, retrying...")
            self._get_url(url, False)

        return result

    def _execute_get_url(self, url, append_sid=True):
        """Low-level function to execute a GET request."""
        url = self._base_url + url
        self._debuglog("GET from URL: " + url)

        if append_sid:
            self._debuglog("Appending access_token (SID: " + self._sid + ") to url")
            url = "%s&sid=%s" % (url, self._sid)

        resp = self._session.get(url, timeout=TIMEOUT)
        return self._handle_response(resp)

    def _execute_post_url(self, url, data, append_sid=True):
        """Low-level function to execute a POST request."""
        url = self._base_url + url
        self._debuglog("POST to URL: " + url)

        if append_sid:
            self._debuglog("Appending access_token (SID: " + self._sid + ") to url")
            data["sid"] = self._sid

        resp = self._session.post(url, data, timeout=TIMEOUT)
        return self._handle_response(resp)

    def _handle_response(self, resp):
        """Ensure response is successful and return body as XML."""
        self._debuglog("Request executed: " + str(resp.status_code))
        if resp.status_code != 200:
            return None

        if resp.headers["Content-Type"] != "text/xml":
            # JSON requests not currently supported
            return None

        xml = etree.fromstring(resp.content)

        auth_passed = xml.xpath('authPassed')
        if auth_passed is not None and len(auth_passed) == 1 and auth_passed[0].text.strip() == "0":
            self._session_error = True
            return None

        return xml

    def get_system_health(self):
        """Obtain the system's overall health."""
        resp = self._get_url("management/manaRequest.cgi?subfunc=sysinfo&sysHealth=1")
        if resp is None:
            return None

        status = resp.xpath("func/ownContent/sysHealth/status")
        if status is None or len(status) == 0:
            return None

        return status[0].text.strip()

    def get_volumes(self):
        """Obtain information about volumes and shared directories."""
        # pylint: disable=line-too-long
        resp = self._get_url("management/chartReq.cgi?chart_func=disk_usage&disk_select=all&include=all")
        # pylint: enable=line-too-long

        if resp is None:
            return None

        volumes = {}
        id_map = {}

        for vol in resp.xpath("volumeList/volume"):
            key = vol.xpath("volumeValue")[0].text.strip()
            label = vol.xpath("volumeLabel")[0].text.strip()

            volumes[label] = {
                "id": key,
                "label": label
            }

            id_map[key] = label

        for vol in resp.xpath("volumeUseList/volumeUse"):
            id_number = vol.xpath("volumeValue")[0].text.strip()

            # Skip any system reserved volumes
            if id_number not in id_map.keys():
                continue

            key = id_map[id_number]

            volumes[key]["free_size"] = int(vol.xpath("free_size")[0].text.strip())
            volumes[key]["total_size"] = int(vol.xpath("total_size")[0].text.strip())

            folder_elements = vol.xpath("folder_element")
            if len(folder_elements) > 0:
                volumes[key]["folders"] = []
                for folder in folder_elements:
                    sharename = folder.xpath("sharename")[0].text.strip()
                    used_size = int(folder.xpath("used_size")[0].text.strip())
                    volumes[key]["folders"].append({"sharename": sharename, "used_size": used_size})

        return volumes

    def get_smart_disk_health(self):
        """Obtain SMART information about each disk."""
        resp = self._get_url("disk/qsmart.cgi?func=all_hd_data")

        if resp is None:
            return None

        disks = []
        for disk in resp.xpath("Disk_Info/entry"):
            disks.append({
                "drive_number": disk.xpath("HDNo")[0].text.strip(),
                "health": disk.xpath("Health")[0].text.strip(),
                "temp_c": int(disk.xpath("Temperature/oC")[0].text.strip()),
                "temp_f": int(disk.xpath("Temperature/oF")[0].text.strip()),
                "capacity": disk.xpath("Capacity")[0].text.strip(),
                "model": disk.xpath("Model")[0].text.strip(),
                "serial": disk.xpath("Serial")[0].text.strip(),
                "type": "hdd" if int(disk.xpath("hd_is_ssd")[0].text.strip()) == 0 else "ssd",
            })

        return disks

    def get_system_stats(self):
        """Obtain core system information and resource utilization."""
        resp = self._get_url("management/manaRequest.cgi?subfunc=sysinfo&hd=no&multicpu=1")

        if resp is None:
            return None

        root = resp.xpath("func/ownContent/root")[0]

        details = {
            "system": {
                "name": root.xpath("server_name")[0].text.strip(),
                "model": resp.xpath("model/displayModelName")[0].text.strip(),
                "serial_number": root.xpath("serial_number")[0].text.strip(),
                "temp_c": int(root.xpath("sys_tempc")[0].text.strip()),
                "temp_f": int(root.xpath("sys_tempf")[0].text.strip()),
                "timezone": root.xpath("timezone")[0].text.strip(),
            },
            "firmware": {
                "version": resp.xpath("firmware/version")[0].text.strip(),
                "build": resp.xpath("firmware/build")[0].text.strip(),
                "patch": resp.xpath("firmware/patch")[0].text.strip(),
                "build_time": resp.xpath("firmware/buildTime")[0].text.strip(),
            },
            "uptime": {
                "days": int(root.xpath("uptime_day")[0].text.strip()),
                "hours": int(root.xpath("uptime_hour")[0].text.strip()),
                "minutes": int(root.xpath("uptime_min")[0].text.strip()),
                "seconds": int(root.xpath("uptime_sec")[0].text.strip()),
            },
            "cpu": {
                "model": root.xpath("cpu_model")[0].text.strip(),
                "usage_percent": float(root.xpath("cpu_usage")[0].text.replace("%", "").strip()),
                "temp_c": int(root.xpath("cpu_tempc")[0].text.strip()),
                "temp_f": int(root.xpath("cpu_tempf")[0].text.strip()),
            },
            "memory": {
                "total": float(root.xpath("total_memory")[0].text.strip()),
                "free": float(root.xpath("free_memory")[0].text.strip()),
            },
            "nics": {},
            "dns": [],
        }

        nic_count = int(root.xpath("nic_cnt")[0].text.strip())
        for nic_index in range(nic_count):
            i = str(nic_index + 1)
            interface = "eth" + str(nic_index)
            status = root.xpath("eth_status" + i)[0].text.strip()
            details["nics"][interface] = {
                "link_status": "Up" if status == "1" else "Down",
                "max_speed": int(root.xpath("eth_max_speed" + i)[0].text.strip()),
                "ip": root.xpath("eth_ip" + i)[0].text.strip(),
                "mask": root.xpath("eth_mask" + i)[0].text.strip(),
                "mac": root.xpath("eth_mac" + i)[0].text.strip(),
                "usage": root.xpath("eth_usage" + i)[0].text.strip(),
                "rx_packets": int(root.xpath("rx_packet" + i)[0].text.strip()),
                "tx_packets": int(root.xpath("tx_packet" + i)[0].text.strip()),
                "err_packets": int(root.xpath("err_packet" + i)[0].text.strip())
            }

        for dns in root.xpath("dnsInfo/DNS_LIST"):
            details["dns"].append(dns.text.strip())

        return details

    def get_bandwidth(self):
        """Obtain the current bandwidth usage speeds."""
        resp = self._get_url("management/chartReq.cgi?chart_func=QSM40bandwidth")

        if resp is None:
            return None

        details = {}

        default = resp.xpath("bandwidth_info/df_gateway")[0].text.strip()

        for item in resp.xpath("bandwidth_info/item"):
            interface = item.xpath("id")[0].text.strip()
            details[interface] = {
                "name": item.xpath("name")[0].text.strip(),
                "rx": int(item.xpath("rx")[0].text.strip()),
                "tx": int(item.xpath("tx")[0].text.strip()),
                "is_default": interface == default
            }

        return details
