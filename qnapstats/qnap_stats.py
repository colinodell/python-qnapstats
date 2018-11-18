"""Module containing multiple classes to obtain QNAP system stats via cgi calls."""
# -*- coding:utf-8 -*-
import xmltodict
import requests


# pylint: disable=too-many-instance-attributes
class QNAPStats:
    """Class containing the main functions."""

    # pylint: disable=too-many-arguments
    def __init__(self, host, port, username, password, debugmode=False, verify_ssl=True, timeout=5):
        """Instantiate a new qnap_stats object."""
        import base64
        self._username = username
        self._password = base64.b64encode(password.encode('utf-8')).decode('ascii')

        self._sid = None
        self._debugmode = debugmode

        self._session_error = False
        self._session = None  # type: requests.Session

        if not (host.startswith("http://") or host.startswith("https://")):
            host = "http://" + host

        self._verify_ssl = verify_ssl
        self._timeout = timeout

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

        self._sid = result["authSid"]
        return True

    def _get_url(self, url, retry_on_error=True, **kwargs):
        """High-level function for making GET requests."""
        self._init_session()

        result = self._execute_get_url(url, **kwargs)
        if (self._session_error or result is None) and retry_on_error:
            self._debuglog("Error occured, retrying...")
            self._get_url(url, False, **kwargs)

        return result

    def _execute_get_url(self, url, append_sid=True, **kwargs):
        """Low-level function to execute a GET request."""
        url = self._base_url + url
        self._debuglog("GET from URL: " + url)

        if append_sid:
            self._debuglog("Appending access_token (SID: " + self._sid + ") to url")
            url = "%s&sid=%s" % (url, self._sid)

        resp = self._session.get(url, timeout=self._timeout, verify=self._verify_ssl)
        return self._handle_response(resp, **kwargs)

    def _execute_post_url(self, url, data, append_sid=True, **kwargs):
        """Low-level function to execute a POST request."""
        url = self._base_url + url
        self._debuglog("POST to URL: " + url)

        if append_sid:
            self._debuglog("Appending access_token (SID: " + self._sid + ") to url")
            data["sid"] = self._sid

        resp = self._session.post(url, data, timeout=self._timeout, verify=self._verify_ssl)
        return self._handle_response(resp, **kwargs)

    def _handle_response(self, resp, force_list=None):
        """Ensure response is successful and return body as XML."""
        self._debuglog("Request executed: " + str(resp.status_code))
        if resp.status_code != 200:
            return None

        if resp.headers["Content-Type"] != "text/xml":
            # JSON requests not currently supported
            return None
        self._debuglog("Response Text: " + resp.text)
        data = xmltodict.parse(resp.content, force_list=force_list)['QDocRoot']

        auth_passed = data['authPassed']
        if auth_passed is not None and len(auth_passed) == 1 and auth_passed == "0":
            self._session_error = True
            return None

        return data

    def get_system_health(self):
        """Obtain the system's overall health."""
        resp = self._get_url("management/manaRequest.cgi?subfunc=sysinfo&sysHealth=1")
        if resp is None:
            return None

        status = resp["func"]["ownContent"]["sysHealth"]["status"]
        if status is None or len(status) == 0:
            return None

        return status

    def get_volumes(self):
        """Obtain information about volumes and shared directories."""
        resp = self._get_url(
            "management/chartReq.cgi?chart_func=disk_usage&disk_select=all&include=all",
            force_list=("volume", "volumeUse", "folder_element")
        )

        if resp is None:
            return None

        volumes = {}
        id_map = {}

        for vol in resp["volumeList"]["volume"]:
            key = vol["volumeValue"]
            label = vol["volumeLabel"] if "volumeLabel" in vol else "Volume " + vol["volumeValue"]

            volumes[label] = {
                "id": key,
                "label": label
            }

            id_map[key] = label

        for vol in resp["volumeUseList"]["volumeUse"]:
            id_number = vol["volumeValue"]

            # Skip any system reserved volumes
            if id_number not in id_map.keys():
                continue

            key = id_map[id_number]

            volumes[key]["free_size"] = int(vol["free_size"])
            volumes[key]["total_size"] = int(vol["total_size"])

            folder_elements = vol["folder_element"]
            if len(folder_elements) > 0:
                volumes[key]["folders"] = []
                for folder in folder_elements:
                    try:
                        sharename = folder["sharename"]
                        used_size = int(folder["used_size"])
                        volumes[key]["folders"].append({"sharename": sharename, "used_size": used_size})
                    except Exception as e:
                        print(e.args)

        return volumes

    def get_smart_disk_health(self):
        """Obtain SMART information about each disk."""
        resp = self._get_url("disk/qsmart.cgi?func=all_hd_data", force_list=("entry"))

        if resp is None:
            return None

        disks = {}
        for disk in resp["Disk_Info"]["entry"]:
            if disk["Model"]:
                disks[disk["HDNo"]] = {
                    "drive_number": disk["HDNo"],
                    "health": disk["Health"],
                    "temp_c": int(disk["Temperature"]["oC"]) if disk["Temperature"]["oC"] is not None else None,
                    "temp_f": int(disk["Temperature"]["oF"]) if disk["Temperature"]["oF"] is not None else None,
                    "capacity": disk["Capacity"],
                    "model": disk["Model"],
                    "serial": disk["Serial"],
                    "type": "ssd" if ("hd_is_ssd" in disk and int(disk["hd_is_ssd"])) else "hdd",
                }

        return disks

    def get_system_stats(self):
        """Obtain core system information and resource utilization."""
        resp = self._get_url(
            "management/manaRequest.cgi?subfunc=sysinfo&hd=no&multicpu=1",
            force_list=("DNS_LIST")
        )

        if resp is None:
            return None

        root = resp["func"]["ownContent"]["root"]

        details = {
            "system": {
                "name": root["server_name"],
                "model": resp["model"]["displayModelName"],
                "serial_number": root["serial_number"],
                "temp_c": int(root["sys_tempc"]),
                "temp_f": int(root["sys_tempf"]),
                "timezone": root["timezone"],
            },
            "firmware": {
                "version": resp["firmware"]["version"],
                "build": resp["firmware"]["build"],
                "patch": resp["firmware"]["patch"],
                "build_time": resp["firmware"]["buildTime"],
            },
            "uptime": {
                "days": int(root["uptime_day"]),
                "hours": int(root["uptime_hour"]),
                "minutes": int(root["uptime_min"]),
                "seconds": int(root["uptime_sec"]),
            },
            "cpu": {
                "model": root["cpu_model"] if "cpu_model" in root else None,
                "usage_percent": float(root["cpu_usage"].replace("%", "")),
                "temp_c": int(root["cpu_tempc"]) if "cpu_tempc" in root else None,
                "temp_f": int(root["cpu_tempf"]) if "cpu_tempf" in root else None,
            },
            "memory": {
                "total": float(root["total_memory"]),
                "free": float(root["free_memory"]),
            },
            "nics": {},
            "dns": [],
        }

        nic_count = int(root["nic_cnt"])
        for nic_index in range(nic_count):
            i = str(nic_index + 1)
            interface = "eth" + str(nic_index)
            status = root["eth_status" + i]
            details["nics"][interface] = {
                "link_status": "Up" if status == "1" else "Down",
                "max_speed": int(root["eth_max_speed" + i]),
                "ip": root["eth_ip" + i],
                "mask": root["eth_mask" + i],
                "mac": root["eth_mac" + i],
                "usage": root["eth_usage" + i],
                "rx_packets": int(root["rx_packet" + i]),
                "tx_packets": int(root["tx_packet" + i]),
                "err_packets": int(root["err_packet" + i])
            }

        for dns in root["dnsInfo"]["DNS_LIST"]:
            details["dns"].append(dns)

        return details

    def get_bandwidth(self):
        """Obtain the current bandwidth usage speeds."""
        resp = self._get_url(
            "management/chartReq.cgi?chart_func=QSM40bandwidth",
            force_list=("item")
        )

        if resp is None:
            return None

        details = {}

        default = resp["bandwidth_info"]["df_gateway"]

        for item in resp["bandwidth_info"]["item"]:
            interface = item["id"]
            details[interface] = {
                "name": item["name"],
                "rx": round(int(item["rx"]) / 5),
                "tx": round(int(item["tx"]) / 5),
                "is_default": interface == default
            }

        return details

    def get_firmware_update(self):
        """Get firmware update version if available."""
        resp = self._get_url("sys/sysRequest.cgi?subfunc=firm_update")
        if resp is None:
            return None

        new_version = resp["func"]["ownContent"]["newVersion"]
        if new_version is None or len(new_version) == 0:
            return None

        return new_version
