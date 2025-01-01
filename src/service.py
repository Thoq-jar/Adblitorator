"""
Adbliterator.py: The service(s) for Adbliterator.
@author: Thoq
@since: December 31st, 2024
"""

import re

from mitmproxy import http

from lib import (AD_KEYWORDS,
                 KNOWN_PATHS,
                 KNOWN_HOSTS,
                 FLASH_EXTENSIONS,
                 FLASH_MIME_TYPES,
                 SETTINGS,
                 write_log)

debug = SETTINGS.get("debug", False)


def parse_html(html_content):
    flash_matches = []

    match = re.search(r'<object\s+.*?type="application/x-shockwave-flash".*?>', html_content, re.IGNORECASE)
    if match:
        flash_matches.append(match.group())

    match = re.search(r'<embed\s+.*?type="application/x-shockwave-flash".*?>', html_content, re.IGNORECASE)
    if match:
        flash_matches.append(match.group())

    match = re.search(r'new\s+Flash\(\s*.*?\)', html_content, re.IGNORECASE)
    if match:
        flash_matches.append(match.group())

    return flash_matches


def request(flow: http.HTTPFlow) -> None:
    for keyword in AD_KEYWORDS:
        if keyword in flow.request.url:
            write_log(f"Blocked Ad Request: {flow.request.url}")
            flow.kill()
            return
    for host in KNOWN_HOSTS:
        if host in flow.request.url:
            write_log(f"Blocked Known Host Request: {flow.request.pretty_url}")
            flow.kill()
            return
    for path in KNOWN_PATHS:
        if path in flow.request.path:
            write_log(f"Blocked Known Path Request: {flow.request.pretty_url}")
            flow.kill()
            return

    if any(ext in flow.request.url for ext in FLASH_EXTENSIONS):
        write_log(f"Blocked Flash Request: {flow.request.url}")
        flow.kill()
        return

    write_log(f"Request: {flow.request.method} {flow.request.pretty_url}")


def response(flow: http.HTTPFlow) -> None:
    if any(mime in flow.response.headers.get("Content-Type", "") for mime in FLASH_MIME_TYPES):
        write_log(f"Blocked Flash Response: {flow.request.pretty_url}")
        flow.kill()
        return

    write_log(f"Response: {flow.response.status_code} {flow.request.pretty_url}")


addons = [
    request,
    response
]
