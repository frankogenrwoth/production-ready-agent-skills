#!/usr/bin/env python3
"""Send an SMS via the Africa's Talking API.

Stdlib-only — no `requests`, no `africastalking` SDK. Reads credentials from
the AT_USERNAME and AT_API_KEY environment variables; the API key is never
written to disk by this script.

Usage:
    AT_USERNAME=<your-username> AT_API_KEY=<your-key> \\
      python3 send_sms.py --to "+256700000000" --message "Hello"

Exit codes:
    0  — at least one recipient was accepted by AT
    1  — credential or input validation failed
    2  — HTTP / API error from AT
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

PROD_ENDPOINT = "https://api.africastalking.com/version1/messaging"
SANDBOX_ENDPOINT = "https://api.sandbox.africastalking.com/version1/messaging"


def validate_phone(num: str) -> str:
    """E.164 check. Returns cleaned number or raises ValueError."""
    cleaned = num.strip().replace(" ", "").replace("-", "")
    if not re.fullmatch(r"\+\d{8,15}", cleaned):
        raise ValueError(
            f"phone number {num!r} is not in E.164 format "
            f"(must start with + and have 8-15 digits, e.g. +256700123456)"
        )
    return cleaned


def post_form(url: str, params: dict, headers: dict, timeout: int = 20) -> tuple[int, dict]:
    """POST application/x-www-form-urlencoded. Returns (status_code, parsed_json)."""
    body = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read().decode("utf-8")
            return resp.status, json.loads(data) if data else {}
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(body_text)
        except json.JSONDecodeError:
            return e.code, {"raw": body_text}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--to", required=True,
                   help="Recipient phone number(s) in E.164 format. Comma-separated for multiple.")
    p.add_argument("--message", required=True,
                   help="The SMS body. Up to 160 chars per single segment; longer messages get split.")
    p.add_argument("--sender-id", default="",
                   help="Optional sender ID registered with your AT account.")
    p.add_argument("--sandbox", action="store_true",
                   help="POST to AT's sandbox endpoint (no real SMS goes out). Default is production.")
    p.add_argument("--enqueue", action="store_true",
                   help="Tell AT to queue the request and return immediately.")
    p.add_argument("--dry-run", action="store_true",
                   help="Print the request that would be sent and exit. Doesn't POST.")
    args = p.parse_args()

    # Credentials from env. Never embedded in the script or read from disk.
    username = os.environ.get("AT_USERNAME", "").strip()
    api_key = os.environ.get("AT_API_KEY", "").strip()
    if not username or not api_key:
        print(
            "error: AT_USERNAME and AT_API_KEY environment variables are required.\n"
            "  Get them from your Africa's Talking dashboard at https://account.africastalking.com/.\n"
            "  Then run with: AT_USERNAME=<u> AT_API_KEY=<k> python3 send_sms.py ...",
            file=sys.stderr,
        )
        return 1

    # Validate each recipient.
    recipients = []
    for raw in args.to.split(","):
        raw = raw.strip()
        if not raw:
            continue
        try:
            recipients.append(validate_phone(raw))
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
    if not recipients:
        print("error: --to must contain at least one phone number", file=sys.stderr)
        return 1

    if not args.message.strip():
        print("error: --message is empty", file=sys.stderr)
        return 1

    endpoint = SANDBOX_ENDPOINT if args.sandbox else PROD_ENDPOINT
    params = {
        "username": username,
        "to": ",".join(recipients),
        "message": args.message,
    }
    if args.sender_id:
        params["from"] = args.sender_id
    if args.enqueue:
        params["enqueue"] = "true"

    headers = {
        "apiKey": api_key,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "User-Agent": "africastalking-sms-skill/1.0",
    }

    if args.dry_run:
        # Surface the request without ever showing the api key.
        masked_headers = {k: ("***" if k.lower() == "apikey" else v) for k, v in headers.items()}
        print(json.dumps({
            "dry_run": True,
            "endpoint": endpoint,
            "headers": masked_headers,
            "body_params": {k: v for k, v in params.items()},
        }, indent=2))
        return 0

    status, body = post_form(endpoint, params, headers)
    if status >= 400:
        print(json.dumps({
            "ok": False,
            "http_status": status,
            "error": body,
        }, indent=2), file=sys.stderr)
        return 2

    # AT response shape: {"SMSMessageData": {"Message": "Sent to 1/1 ...", "Recipients": [...]}}
    message_data = body.get("SMSMessageData", {})
    summary_text = message_data.get("Message", "")
    raw_recipients = message_data.get("Recipients", [])

    accepted = 0
    details = []
    cost_total = "0"
    for r in raw_recipients:
        # AT success codes: 100 = Processed, 101 = Sent, 102 = Queued. 4xx = failures.
        is_ok = r.get("statusCode") in (100, 101, 102)
        if is_ok:
            accepted += 1
        details.append({
            "number": r.get("number"),
            "status": r.get("status"),
            "status_code": r.get("statusCode"),
            "cost": r.get("cost"),
            "message_id": r.get("messageId"),
        })
        # Cost is a string like "KES 0.8000"; AT returns one cost per recipient
        if r.get("cost"):
            cost_total = r["cost"]  # for single recipient simple display

    output = {
        "ok": accepted > 0,
        "endpoint": "sandbox" if args.sandbox else "production",
        "summary": summary_text,
        "recipients": len(recipients),
        "accepted": accepted,
        "details": details,
    }
    print(json.dumps(output, indent=2))
    return 0 if accepted > 0 else 2


if __name__ == "__main__":
    sys.exit(main())
