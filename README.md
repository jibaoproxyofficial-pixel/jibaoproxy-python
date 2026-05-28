# jibaoproxy-python

Official Python SDK for **[JiBao Proxy](https://jibaoproxy.com)** — 72M+ residential IPs across 200+ countries, plus datacenter, mobile, and static proxies.

```bash
pip install jibaoproxy
```

## Quick start

Get your sub-account ID from [member.jibaoproxy.com → Dynamic Residential](https://member.jibaoproxy.com), then:

```python
import requests
from jibaoproxy import JiBaoProxy

client = JiBaoProxy(username="c83d7fb7-afe7fa00", password="wifi")

# Rotating: new IP every call
for _ in range(3):
    r = requests.get("https://httpbin.org/ip", proxies=client.session())
    print(r.json()["origin"])
```

## Sticky sessions

Re-use the same exit IP across requests (login flows, carts, etc.):

```python
client = JiBaoProxy(username="c83d7fb7-afe7fa00")
proxies = client.sticky()      # holds one session
# ... many requests on the same IP ...
client.rotate()                # force a fresh exit IP
```

## Geo targeting

```python
# hk, us, jp, uk, de, sg, kr, tw, ca, au
client = JiBaoProxy(username="...", area="us")
requests.get("https://httpbin.org/ip", proxies=client.session())
```

See [`jibaoproxy.geo.AREAS`](jibaoproxy/geo.py) for the full list.

## SOCKS5

```python
client = JiBaoProxy(username="...", protocol="socks5")
# requests needs `requests[socks]` for SOCKS5
```

## API extract (IP-whitelist auth)

If you prefer IP whitelisting over user:pass:

```python
from jibaoproxy import extract_ips

ips = extract_ips(token="YOUR_API_TOKEN", qty=10, area="us", type="wifi")
# ['1.2.3.4:8080', '5.6.7.8:8080', ...]
```

## Async (httpx)

```bash
pip install jibaoproxy[async]
```

```python
import httpx
from jibaoproxy import JiBaoProxy

client = JiBaoProxy(username="...")
async with httpx.AsyncClient(proxies=client.session()["http"]) as http:
    r = await http.get("https://httpbin.org/ip")
```

## Proxy types

| `password` | What you get          | Price  |
|------------|-----------------------|--------|
| `wifi`     | Residential, rotating | $10/GB |
| `dat`      | Datacenter, rotating  | $1/GB  |
| `5g`       | Mobile, rotating      | $15/GB |

Static (per-IP, monthly) plans are also available — see [jibaoproxy.com](https://jibaoproxy.com).

## $5 free on signup

[Create an account at jibaoproxy.com](https://jibaoproxy.com) — every new user gets $5 of dynamic traffic, no card required.

## License

MIT
