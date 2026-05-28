"""JiBao Proxy client — generates proxy URLs and requests-compatible proxies dicts."""

from __future__ import annotations

import secrets
import string
from dataclasses import dataclass, field
from typing import Optional

from .geo import AREAS, PROTOCOLS, TYPES


def _new_session_id(length: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits
    return "L" + "".join(secrets.choice(alphabet) for _ in range(length))


@dataclass
class JiBaoProxy:
    """Generate JiBao Proxy URLs for use with requests, httpx, aiohttp, curl, etc.

    Args:
        username: Your sub-account ID, e.g. "c83d7fb7-afe7fa00" (from member.jibaoproxy.com).
        password: Proxy type — "wifi" residential, "dat" datacenter, "5g" mobile.
        area: Access-point area code (see jibaoproxy.geo.AREAS). Default "hk".
        protocol: "http" or "socks5". Default "http".
        port: Override port. Default 930.
        domain: Override domain root. Default "jibao.vip".
    """

    username: str
    password: str = "wifi"
    area: str = "hk"
    protocol: str = "http"
    port: int = 930
    domain: str = "jibao.vip"
    _current_session: Optional[str] = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.password not in TYPES:
            raise ValueError(f"password must be one of {list(TYPES)}, got {self.password!r}")
        if self.protocol not in PROTOCOLS:
            raise ValueError(f"protocol must be one of {PROTOCOLS}, got {self.protocol!r}")

    @property
    def host(self) -> str:
        return f"{self.area}.{self.domain}"

    def url(self, session_id: Optional[str] = None) -> str:
        sid = session_id or _new_session_id()
        return f"{self.protocol}://{self.username}-{sid}:{self.password}@{self.host}:{self.port}"

    def session(self, session_id: Optional[str] = None) -> dict:
        """Return a `proxies` dict for requests/httpx. Pass same session_id for sticky."""
        u = self.url(session_id)
        return {"http": u, "https": u}

    def sticky(self, session_id: Optional[str] = None) -> dict:
        """Same exit IP across calls — held in self._current_session."""
        if session_id is None and self._current_session is None:
            self._current_session = _new_session_id()
        elif session_id is not None:
            self._current_session = session_id
        return self.session(self._current_session)

    def rotate(self) -> dict:
        """Force a new session/exit IP."""
        self._current_session = _new_session_id()
        return self.session(self._current_session)
