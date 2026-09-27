import pytest
import platform
import psutil
import sys
import logging
import server_health_checker
from pathlib import Path
from types import SimpleNamespace
from server_health_checker import (cpu_check, 
ram_check, 
disk_check, 
overall_status, 
get_exit_code, 
validate_config, 
load_config, 
parse_args,
process_checks, 
get_disk_path, 
get_system_metrics,
log_result,)

@pytest.mark.parametrize(
    "cpu, warning, critical, expected",
    [
        (50, 80, 90, 'OK'), 
        (85, 80, 90, 'WARNING'), 
        (95, 80, 90, 'CRITICAL')],
)

def test_cpu_check(cpu, warning, critical, expected):
    assert cpu_check(cpu, warning, critical) == expected


@pytest.mark.parametrize(
    "ram, warning, critical, expected",
    [
        (50, 80, 90, 'OK'), 
        (85, 80, 90, 'WARNING'), 
        (95, 80, 90, 'CRITICAL')],
)

def test_ram_check(ram, warning, critical, expected):
    assert ram_check(ram, warning, critical) == expected


@pytest.mark.parametrize(
    "disk, warning, critical, expected",
    [
        (70, 80, 90, 'OK'), 
        (85, 80, 90, 'WARNING'), 
        (95, 80, 90, 'CRITICAL')],
)

def test_disk_check(disk, warning, critical, expected):
    assert disk_check(disk, warning, critical) == expected


@pytest.mark.parametrize(
    "crd, expected",
    [(
    {"cpu": "OK", "ram": "OK", "disk": "OK"},
    "OK"
), (
    {"cpu": "OK", "ram": "OK", "disk": "WARNING"},
    "WARNING"
), (
    {"cpu": "OK", "ram": "CRITICAL", "disk": "OK"},
    "CRITICAL"
), (
    {"cpu": "WARNING", "ram": "CRITICAL", "disk": "OK"},
    "CRITICAL"
)],
)

def test_overall_status(crd, expected):
    assert overall_status(crd) == expected


@pytest.mark.parametrize(
    "status, expected",
    [
    ('OK', 0),
    ('WARNING', 1), 
    ('CRITICAL', 2), 
    ('UNKNOWN', 3),
    ],
)

def test_get_exit_code(status, expected):
    assert get_exit_code(status) == expected


@pytest.mark.parametrize(
    "config, expected",
    [
        ({"disk": {"warning": 90, "critical": 95}}, False),
        ({"resources": {"warning": 80, "critical": 90}}, False),
        ({"resources": {"critical": 90}, "disk": {"critical": 95}}, False),
        ({"resources": {"warning": "abc", "critical": 95}, "disk": {"warning": 90, "critical": 95}}, False),
        ({"resources": {"warning": 0, "critical": 90}, "disk": {"warning": 90, "critical": 95}}, False),
        ({"resources": {"warning": 101, "critical": 95}, "disk": {"warning": 90, "critical": 95}}, False),
        ({"resources": {"warning": 95, "critical": 80}, "disk": {"warning": 90, "critical": 95}}, False),
        ({"resources": {"warning": 80, "critical": 95}, "disk": {"warning": 90, "critical": 95}}, True)
    ]
)

def test_validate_config(config, expected):
    assert validate_config(config) == expected


def test_load_config(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        'resources:\n'
        '    warning: 80\n'
        '    critical: 90\n'
        'disk:\n'
        '    warning: 90\n'
        '    critical: 95'
    )
    result = load_config(config_path)
    assert result == {
    "resources": {
        "warning": 80,
        "critical": 90
    },
    "disk": {
        "warning": 90,
        "critical": 95
    }
}

def test_load_config_file_not_found():
    config_path = Path('notfound.yaml')
    with pytest.raises(SystemExit) as exc_info:
        load_config(config_path)
    assert exc_info.value.code == 4


def test_parse_args(monkeypatch):
    monkeypatch.setattr(
    sys,
    "argv",
    [
    "server_health_checker.py",
    "-c",
    "config.yaml"
]
)
    result = parse_args()
    assert result == (Path("config.yaml"), False)

@pytest.mark.parametrize(
    "cpu, ram, disk, expected_status, expected_exit_code",
    [(12, 37, 29, 'OK', 0), (80, 80, 90, 'WARNING', 1), (91, 91, 96, 'CRITICAL', 2)]
)
def test_process_checks(cpu, ram, disk, expected_status, expected_exit_code):
    thresholds = {
        "resources_warning": 80,
        "resources_critical": 90,
        "disk_warning": 90,
        "disk_critical": 95,
    }
    result, exit_code = process_checks(cpu, ram, disk, thresholds)
    assert expected_status in result
    assert exit_code == expected_exit_code


@pytest.mark.parametrize(
    "os_name, expected_path",
    [
        ("Linux", "/home"),
        ("Windows", "C:\\"),
        ("Darwin", "/Users"),
    ]
)

def test_get_disk_path(monkeypatch, expected_path, os_name):
    monkeypatch.setattr(platform, 'system', lambda: os_name)
    result = get_disk_path()
    assert result == expected_path

def test_get_disk_path_another_os(monkeypatch):
    monkeypatch.setattr(platform, 'system', lambda: 'FreeBSD')
    with pytest.raises(SystemExit) as exc_info:
        get_disk_path()
    assert exc_info.value.code == 1


def test_get_system_metrics(monkeypatch):
    monkeypatch.setattr(psutil, 'cpu_percent', lambda interval: 25.5)
    virtual_memory = SimpleNamespace(percent=63.2)
    disk_usage = SimpleNamespace(percent=47.8)
    monkeypatch.setattr(psutil, 'virtual_memory', lambda: virtual_memory)
    monkeypatch.setattr(psutil, 'disk_usage', lambda path: disk_usage)
    assert get_system_metrics('/home') == (25.5, 63.2, 47.8)

@pytest.mark.parametrize(
        'result, log_func, mess, percent',
        [('CRITICAL', 'error', 'CPU usage: 95% - CRITICAL', 95),
         ('WARNING', 'warning', 'CPU usage: 85% - WARNING', 85),
         ('OK', 'info', 'CPU usage: 50% - OK', 50)] 
)
def test_log_result(monkeypatch, result, log_func, mess, percent):
    messages = []
    monkeypatch.setattr(logging, log_func, lambda message: messages.append(message))
    log_result('CPU', percent, result)
    assert messages == [mess]


def test_main(monkeypatch):
    monkeypatch.setattr(server_health_checker, 'parse_args', lambda: (Path('config.yaml'), True))
    monkeypatch.setattr(server_health_checker, 'load_config', lambda cfg_path: {
            'resources': {'warning': 80, 'critical': 90},
            'disk': {'warning': 90, 'critical': 95}
        }
        )
    monkeypatch.setattr(server_health_checker, 'validate_config', lambda config: True)
    monkeypatch.setattr(server_health_checker, 'get_disk_path', lambda: '/home')
    monkeypatch.setattr(server_health_checker, 'get_system_metrics',lambda disk_path: (25.5, 63.2, 47.8))
    monkeypatch.setattr(server_health_checker, 'process_checks', lambda cpu, ram, disk, thresholds: ('test result', 0))
    with pytest.raises(SystemExit) as exc_info:
        server_health_checker.main()
    assert exc_info.value.code == 0