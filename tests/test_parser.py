"""
Tests for parse_nmap: runs against tests/fixtures/sample_scan.xml.

Run:  pytest tests/test_parser.py -v

The fixture has 3 hosts for testing:
  10.0.0.5  UP, 2 open ports, full service+cpe+script, OS detected, has a MAC addr
  10.0.0.6  UP, 1 filtered port with NO <service> (tests Optional/None)
  10.0.0.99 DOWN, no ports, no os (tests empty tuples)
"""
from pathlib import Path
from pprint import pprint
import pytest


from pentestupgrade.adapters.inbound.nmap_adapter import parse_nmap
from pentestupgrade.domain.enums import Host_State, Port_State


@pytest.fixture
def sample_xml() -> str:
    """The synthetic scan output, shared by every test that names it."""
    return (Path(__file__).parent / "fixtures" / "sample_scan.xml").read_text()


def test_parses_all_three_hosts(sample_xml):
    hosts = parse_nmap(sample_xml)
    assert len(hosts) == 3

def test_returns_a_tuple(sample_xml):
    hosts = parse_nmap(sample_xml)
    assert isinstance(hosts, tuple)


# ── host 1: fully-populated ────────────────────────────────────────────────
def test_first_host_basics(sample_xml):
    host = parse_nmap(sample_xml)[0]
    assert host.ip_address == "10.0.0.5"
    assert host.ip_protocol == "ipv4"
    assert host.host_states == Host_State.UP

def test_first_host_ports(sample_xml):
    host = parse_nmap(sample_xml)[0]
    assert len(host.ports) == 2
    ssh = host.ports[0]
    assert ssh.port_number == "22"
    assert ssh.port_protocol == "tcp"
    assert ssh.state == Port_State.OPEN

def test_first_host_service(sample_xml):
    ssh = parse_nmap(sample_xml)[0].ports[0]
    assert ssh.port_service is not None
    assert ssh.port_service.name == "ssh"
    assert ssh.port_service.product == "OpenSSH"
    assert ssh.port_service.version == "8.2p1"

def test_first_host_cpes(sample_xml):
    ssh = parse_nmap(sample_xml)[0].ports[0]
    assert ssh.port_service.cpe == (
        "cpe:/a:openbsd:openssh:8.2p1",
        "cpe:/o:linux:linux_kernel",
    )

def test_first_host_script_output(sample_xml):
    ssh = parse_nmap(sample_xml)[0].ports[0]
    assert ssh.port_script_output is not None
    assert "RSA" in ssh.port_script_output

def test_first_host_os(sample_xml):
    host = parse_nmap(sample_xml)[0]
    assert len(host.os) == 1
    assert host.os[0].os_name == "Linux 5.0 - 5.14"
    assert host.os[0].os_match_accuracy == "95"
    assert host.os[0].os_raw_finger_print is not None


# ── host 2: port with NO service (the Optional/None case) ──────────────────
def test_second_host_filtered_port_no_service(sample_xml):
    host = parse_nmap(sample_xml)[1]
    assert host.ip_address == "10.0.0.6"
    assert len(host.ports) == 1
    port = host.ports[0]
    assert port.state == Port_State.FILTERED
    assert port.port_service is None    


# ── host 3: DOWN, empty (the empty-tuple case) ─────────────────────────────
def test_third_host_down_empty(sample_xml):
    host = parse_nmap(sample_xml)[2]
    assert host.ip_address == "10.0.0.99"
    assert host.host_states == Host_State.DOWN
    assert host.ports == ()             
    assert host.os == ()                 


# ── error handling ─────────────────────────────────────────────────────────
def test_malformed_xml_raises():
    with pytest.raises(Exception):        
        parse_nmap("this is not xml <<<")

def test_empty_scan_returns_empty_tuple():
    xml = '<?xml version="1.0"?><nmaprun></nmaprun>'
    assert parse_nmap(xml) == ()         

