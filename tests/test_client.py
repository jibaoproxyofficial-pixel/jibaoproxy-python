import re
import pytest
from jibaoproxy import JiBaoProxy


def test_url_shape():
    c = JiBaoProxy(username="acct", password="wifi", area="us")
    assert c.url("Labc12345") == "http://acct-Labc12345:wifi@us.jibao.vip:930"


def test_session_dict():
    c = JiBaoProxy(username="acct")
    s = c.session("Labc12345")
    assert s["http"] == s["https"]
    assert s["http"].startswith("http://acct-Labc12345:wifi@hk.jibao.vip:930")


def test_rotate_changes_id():
    c = JiBaoProxy(username="acct")
    assert c.sticky()["http"] != c.rotate()["http"]


def test_sticky_stable():
    c = JiBaoProxy(username="acct")
    assert c.sticky()["http"] == c.sticky()["http"]


def test_random_ids_unique():
    c = JiBaoProxy(username="acct")
    ids = {re.search(r"acct-(L\w+):", c.url()).group(1) for _ in range(20)}
    assert len(ids) == 20


def test_invalid_password():
    with pytest.raises(ValueError):
        JiBaoProxy(username="acct", password="bogus")


def test_socks5():
    c = JiBaoProxy(username="acct", protocol="socks5")
    assert c.url("Labc12345").startswith("socks5://acct-Labc12345:wifi@")
