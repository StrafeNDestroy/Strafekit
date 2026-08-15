from pathlib import Path
from pprint import pprint
from pentestupgrade.adapters.inbound.nmap_adapter import parse_nmap  # match your real path

xml = (Path(__file__).parent.parent / "tests" / "fixtures" / "sample_scan.xml").read_text()
for host in parse_nmap(xml):
    pprint(host)
