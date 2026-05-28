"""API-extract helper for JiBao Proxy's IP-whitelist endpoint."""

from __future__ import annotations

from typing import List

import requests

EXTRACT_URL = "https://member.jibaoproxy.com/api/user_get_ip_list"


def extract_ips(
    token: str,
    qty: int = 1,
    type: str = "wifi",
    area: str = "hk",
    protocol: str = "http",
    format: str = "text",
    is_rand: int = 0,
    timeout: float = 10.0,
) -> List[str]:
    """Fetch a batch of `ip:port` strings from JiBao's extract API.

    Requires your IP to be whitelisted in member.jibaoproxy.com.
    """
    params = {
        "token": token, "type": type, "qty": qty, "format": format,
        "protocol": protocol, "area": area, "is_rand": is_rand, "output": 1,
    }
    r = requests.get(EXTRACT_URL, params=params, timeout=timeout)
    r.raise_for_status()
    if format == "json":
        data = r.json()
        return data.get("data", []) if isinstance(data, dict) else data
    return [line.strip() for line in r.text.splitlines() if line.strip()]
