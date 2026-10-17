"""Functional tests where the QNAP responses are mocked"""
# -*- coding:utf-8 -*-
import base64
import json
import os
import re
from unittest.mock import call, patch
import qnapstats
import responses


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


response_directory = os.path.join(os.path.dirname(__file__), 'responses')
models = get_immediate_subdirectories(response_directory)


def add_mock_responses(rsps, directory):
    rsps.add(responses.POST,
             'http://localhost:8080/cgi-bin/authLogin.cgi',
             body=file_get_contents(directory, 'login.xml'),
             status=200,
             content_type='text/xml')
    if file_get_contents(directory, "login_with_get.xml"):
        pwd = base64.b64encode("correcthorsebatterystaple".encode('utf-8')).decode('ascii')
        rsps.add(responses.GET,
                 'http://localhost:8080/cgi-bin/authLogin.cgi?user=admin&pwd=' + pwd,
                 body=file_get_contents(directory, 'login_with_get.xml'),
                 status=200,
                 content_type='text/xml')
    xml = file_get_contents(directory, 'bandwidth.xml')
    if xml is not None:
        rsps.add(responses.GET,
                 'http://localhost:8080/cgi-bin/management/chartReq.cgi?chart_func=QSM40bandwidth&sid=12345',
                 match_querystring=True,
                 body=xml,
                 status=200,
                 content_type='text/xml')

    xml = file_get_contents(directory, 'bandwidth2.xml')
    if xml is not None:
        rsps.add(responses.GET,
                 'http://localhost:8080/cgi-bin/management/chartReq.cgi?chart_func=bandwidth&sid=12345',
                 match_querystring=True,
                 body=xml,
                 status=200,
                 content_type='text/xml')

    xml = file_get_contents(directory, 'systemhealth.xml')
    if xml is not None:
        rsps.add(responses.GET,
                 'http://localhost:8080/cgi-bin/management/manaRequest.cgi?subfunc=sysinfo&sysHealth=1&sid=12345',
                 match_querystring=True,
                 body=file_get_contents(directory, 'systemhealth.xml'),
                 status=200,
                 content_type='text/xml')

    xml = file_get_contents(directory, 'volumes.xml')
    if xml is not None:
        rsps.add(responses.GET,
                 'http://localhost:8080/cgi-bin/management/chartReq.cgi?chart_func=disk_usage&disk_select=all&include=all&sid=12345',  # noqa: E501
                 match_querystring=True,
                 body=file_get_contents(directory, 'volumes.xml'),
                 status=200,
                 content_type='text/xml')

    xml = file_get_contents(directory, 'smartdiskhealth.xml')
    if xml is not None:
        rsps.add(responses.GET,
                 'http://localhost:8080/cgi-bin/disk/qsmart.cgi?func=all_hd_data&sid=12345',
                 match_querystring=True,
                 body=file_get_contents(directory, 'smartdiskhealth.xml'),
                 status=200,
                 content_type='text/xml')

    xml = file_get_contents(directory, 'systemstats.xml')
    if xml is not None:
        rsps.add(responses.GET,
                 'http://localhost:8080/cgi-bin/management/manaRequest.cgi?subfunc=sysinfo&hd=no&multicpu=1&sid=12345',
                 match_querystring=True,
                 body=file_get_contents(directory, 'systemstats.xml'),
                 status=200,
                 content_type='text/xml')

    xml = file_get_contents(directory, 'firmwareupdate.xml')
    if xml is not None:
        rsps.add(responses.GET,
                 'http://localhost:8080/cgi-bin/sys/sysRequest.cgi?subfunc=firm_update&sid=12345',
                 match_querystring=True,
                 body=file_get_contents(directory, 'firmwareupdate.xml'),
                 status=200,
                 content_type='text/xml')


def file_get_contents(directory, file):
    file = os.path.join(response_directory, directory, file)
    if not os.path.exists(file):
        return None

    with open(file, 'r') as myfile:
        return myfile.read()


# A successful retry must return the retried response, not the failed first attempt.
qnap = qnapstats.QNAPStats("localhost", 8080, "admin", "correcthorsebatterystaple")
with patch.object(qnap, "_init_session"), \
        patch.object(qnap, "_execute_get_url", side_effect=[None, {"ok": "1"}]) as execute_get_url:
    assert qnap._get_url("some/url.cgi") == {"ok": "1"}
    assert execute_get_url.call_count == 2

with patch.object(qnap, "_init_session"), \
        patch.object(qnap, "_execute_get_url", return_value=None) as execute_get_url:
    assert qnap._get_url("some/url.cgi") is None
    assert execute_get_url.call_count == 2


# Missing NIC fields must not prevent other interfaces from being returned.
nic_fields = (
    "eth_status", "eth_max_speed", "eth_ip", "eth_mask", "eth_mac",
    "eth_usage", "rx_packet", "tx_packet", "err_packet",
)
missing_nic_directory = 'TS-EC1280U-4.5.2-missing-nic'
for missing_field in nic_fields:
    qnap = qnapstats.QNAPStats("localhost", 8080, "admin", "correcthorsebatterystaple")
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        add_mock_responses(rsps, missing_nic_directory)
        # Leave an incomplete interface in the middle, as well as the absent
        # seventh interface, to check that later complete interfaces survive.
        xml = file_get_contents(missing_nic_directory, 'systemstats.xml')
        xml = re.sub(r"<" + missing_field + r"3>.*?</" + missing_field + r"3>", "", xml)
        rsps.replace(responses.GET,
                     'http://localhost:8080/cgi-bin/management/manaRequest.cgi'
                     '?subfunc=sysinfo&hd=no&multicpu=1&sid=12345',
                     match_querystring=True,
                     body=xml,
                     status=200,
                     content_type='text/xml')
        expected = json.loads(file_get_contents(missing_nic_directory, 'systemstats.json'))
        del expected["nics"]["eth2"]
        assert qnap.get_system_stats() == expected


primary_call = call("management/chartReq.cgi?chart_func=QSM40bandwidth", force_list="item")
fallback_call = call("management/chartReq.cgi?chart_func=bandwidth")
bandwidth_response = {
    "bandwidth_info": {
        "df_gateway": "eth0",
        "eth_index_list": "0,1,2,3,4,5",
        "wlan_index_list": None,
    }
}
expected_bandwidth = {}
for index in range(6):
    interface_id = "eth" + str(index)
    bandwidth_response["bandwidth_info"][interface_id] = {
        "name": interface_id,
        "rx": str(500 * (index + 1)),
        "tx": str(250 * (index + 1)),
    }
    expected_bandwidth[interface_id] = {
        "name": interface_id,
        "rx": 100 * (index + 1),
        "tx": 50 * (index + 1),
        "is_default": index == 0,
    }

qnap = qnapstats.QNAPStats("localhost", 8080, "admin", "correcthorsebatterystaple")
for primary_response in (None, {}, {"model": "TVS-1677X"}):
    with patch.object(qnap, "_get_url", side_effect=[primary_response, bandwidth_response]) as get_url:
        assert qnap.get_bandwidth() == expected_bandwidth
        assert get_url.call_args_list == [primary_call, fallback_call]

with patch.object(qnap, "_get_url", return_value=bandwidth_response) as get_url:
    assert qnap.get_bandwidth() == expected_bandwidth
    assert get_url.call_args_list == [primary_call]

with patch.object(qnap, "_get_url", return_value=None) as get_url:
    assert qnap.get_bandwidth() is None
    assert get_url.call_args_list == [primary_call, fallback_call]


for model_directory in models:
    qnap = qnapstats.QNAPStats("localhost", 8080, "admin", "correcthorsebatterystaple")
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        add_mock_responses(rsps, model_directory)

        bandwidth = file_get_contents(model_directory, 'bandwidth.json')
        if bandwidth is not None:
            assert json.dumps(qnap.get_bandwidth(), sort_keys=True) == bandwidth.rstrip()

        smartdiskhealth = file_get_contents(model_directory, 'smartdiskhealth.json')
        if smartdiskhealth is not None:
            assert json.dumps(qnap.get_smart_disk_health(), sort_keys=True) == smartdiskhealth

        systemhealth = file_get_contents(model_directory, 'systemhealth.json')
        if systemhealth is not None:
            assert json.dumps(qnap.get_system_health(), sort_keys=True) == systemhealth

        systemstats = file_get_contents(model_directory, 'systemstats.json')
        if systemstats is not None:
            assert json.dumps(qnap.get_system_stats(), sort_keys=True) == systemstats.rstrip()

        volumes = file_get_contents(model_directory, 'volumes.json')
        if volumes is not None:
            assert json.dumps(qnap.get_volumes(), sort_keys=True) == volumes

        firmwareupdate = file_get_contents(model_directory, 'firmwareupdate.json')
        if firmwareupdate is not None:
            assert json.dumps(qnap.get_firmware_update(), sort_keys=True) == firmwareupdate
