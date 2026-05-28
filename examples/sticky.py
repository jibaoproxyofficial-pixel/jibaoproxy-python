"""Sticky session — same exit IP across multiple requests."""
import requests
from jibaoproxy import JiBaoProxy

client = JiBaoProxy(username="YOUR_SUBACCOUNT_ID", area="us")
proxies = client.sticky()
for path in ("/ip", "/headers"):
    print(path, requests.get(f"https://httpbin.org{path}", proxies=proxies, timeout=15).json())

client.rotate()
print("rotated:", requests.get("https://httpbin.org/ip", proxies=client.session()).json())
