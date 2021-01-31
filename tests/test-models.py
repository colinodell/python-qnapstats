"""Functional tests where the QNAP responses are mocked"""
# -*- coding:utf-8 -*-
import json
import os
import qnapstats
import responses


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


response_directory = os.path.join(os.path.dirname(__file__), 'responses')
models = get_immediate_subdirectories(response_directory)


def add_mock_responses(rsps, directory):
    rsps.add(responses.GET,
             'http://localhost:8080/cgi-bin/authLogin.cgi',
             body=file_get_contents(directory, 'login.xml'),
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


for model_directory in models:
    qnap = qnapstats.QNAPStats("localhost", 8080, "admin", "correcthorsebatterystaple")
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        add_mock_responses(rsps, model_directory)

        bandwidth = file_get_contents(model_directory, 'bandwidth.json')
        if bandwidth is not None:
            assert json.dumps(qnap.get_bandwidth(), sort_keys=True) == bandwidth

        smartdiskhealth = file_get_contents(model_directory, 'smartdiskhealth.json')
        if smartdiskhealth is not None:
            assert json.dumps(qnap.get_smart_disk_health(), sort_keys=True) == smartdiskhealth

        systemhealth = file_get_contents(model_directory, 'systemhealth.json')
        if systemhealth is not None:
            assert json.dumps(qnap.get_system_health(), sort_keys=True) == systemhealth

        systemstats = file_get_contents(model_directory, 'systemstats.json')
        if systemstats is not None:
            assert json.dumps(qnap.get_system_stats(), sort_keys=True) == systemstats

        volumes = file_get_contents(model_directory, 'volumes.json')
        if volumes is not None:
            assert json.dumps(qnap.get_volumes(), sort_keys=True) == volumes

        firmwareupdate = file_get_contents(model_directory, 'firmwareupdate.json')
        if firmwareupdate is not None:
            assert json.dumps(qnap.get_firmware_update(), sort_keys=True) == firmwareupdate
