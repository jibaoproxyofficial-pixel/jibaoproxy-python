"""Rotating residential IPs — new exit IP per request."""
import requests
from jibaoproxy import JiBaoProxy

client = JiBaoProxy(username="YOUR_SUBACCOUNT_ID", password="wifi", area="us")
for _ in range(5):
    r = requests.get("https://httpbin.org/ip", proxies=client.session(), timeout=15)
    print(r.json()["origin"])
