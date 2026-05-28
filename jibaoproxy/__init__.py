"""JiBao Proxy Python SDK.

Quick start:
    from jibaoproxy import JiBaoProxy
    client = JiBaoProxy(username="your-account-id", password="wifi")
    requests.get("https://httpbin.org/ip", proxies=client.session())
"""
from .client import JiBaoProxy
from .extract import extract_ips
from .geo import AREAS, PROTOCOLS, TYPES

__version__ = "0.1.0"
__all__ = ["JiBaoProxy", "extract_ips", "AREAS", "PROTOCOLS", "TYPES"]
