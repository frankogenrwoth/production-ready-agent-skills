---
name: africastalking-sms
description: Send an SMS via the Africa's Talking SMS API. Use whenever the user wants to send a text message, alert, OTP, notification, "send SMS to <number>", or any phrasing that involves delivering a short message to a mobile phone in Africa. The skill posts to Africa's Talking's REST endpoint and returns the delivery status.
license: MIT
compatibility: Requires Python 3 (stdlib only) and the AT_USERNAME + AT_API_KEY + AT_SENDER_ID environment variables.
metadata:
  author: David Okwii
  venue: Africa's Talking East Africa Hub, Kampala
  version: "1.0"
---

# Africa's Talking SMS

A skill for sending one or more SMS messages via the [Africa's Talking](https://africastalking.com/) bulk SMS API.

## When to use

Trigger this skill when the user asks to:

- "Send an SMS to +256… saying …"
- "Text my number with …"
- "Notify the team via SMS"
- "Send an OTP to …"
- "Broadcast … to the following numbers"
- Anything else where the goal is delivering a short message to a mobile phone

If the user just wants to send a *file* or *long content*, this is the wrong skill — use email or chat.

## Required environment variables

Three env vars must be set before invoking the skill:

| Variable | What it is | Example |
|---|---|---|
| `AT_USERNAME` | Your Africa's Talking account username (or the literal string `sandbox`) | `odukar` |
| `AT_API_KEY` | The API key from your Africa's Talking dashboard | `atsk_xxxxx…` |
| `AT_SENDER_ID` | A sender ID registered with your AT account — alphanumeric (e.g. `DIGNITED`) or a shortcode | `DIGNITED` |

If any are missing, the script errors out clearly and refuses to send. The sender ID is **required** because AT (and Uganda's regulator) won't reliably deliver bulk SMS without one — without it, messages either get dropped or sent under a generic pool shortcode that recipients distrust.

**Never paste the API key into a `SKILL.md` or commit it to git** — that's a credential-leak landmine.

## How to use

```bash
python3 <skill-dir>/scripts/send_sms.py \
  --to "+256700000000" \
  --message "Hello from a Claude Code skill at AT Kampala"
```

The script substitutes the skill's directory at runtime — Claude Code shows the `Base directory for this skill: …` line in its system prompt.

### Common flags

- `--to "<number>"` — required. E.164 format with `+` and country code (e.g. `+254700112233`). Multiple numbers comma-separated.
- `--message "<text>"` — required. Plain text. Up to 160 chars per single SMS; longer messages get split and billed per segment.
- `--sender-id "<id>"` — overrides `AT_SENDER_ID` for a single call. The sender ID itself is required — set it via env var or this flag.
- `--sandbox` — optional. POSTs to the sandbox endpoint instead of production. Useful for testing — the API call returns success but no actual SMS goes out. Defaults to production (real SMS).
- `--enqueue` — optional. Tells AT to queue the request and return immediately rather than waiting for telco acknowledgement. Useful for bulk sends.

## Workflow

1. **Validate the phone number.** Must start with `+` and have 10–15 digits. If the user provided a number without `+`, ask for clarification — don't guess the country code.
2. **Confirm the message content.** If it contains anything sensitive (OTP, password reset link), echo back to the user before sending.
3. **Run the script** with `--to` and `--message`.
4. **Read the script's JSON output.** Each recipient gets a status code (101 = success, 102 = queued for delivery, 401–406 = various failure modes — see `references/STATUS_CODES.md` if present, or [AT's status code docs](https://developers.africastalking.com/docs/sms/sending/status_codes)).
5. **Report to the user**: how many sent, total cost (in user's account currency), any failed numbers and why.

## Examples

### Single recipient

User: *"Send an SMS to +256700123456 saying 'Your OTP is 4829'"*

Run:
```bash
python3 scripts/send_sms.py --to "+256700123456" --message "Your OTP is 4829"
```

Expected output (JSON):
```json
{
  "ok": true,
  "recipients": 1,
  "sent": 1,
  "cost_total": "KES 0.8000",
  "details": [
    {"number": "+256700123456", "status": "Success", "cost": "KES 0.8000", "messageId": "ATXid_..."}
  ]
}
```

### Multiple recipients

User: *"Send 'Meeting moved to 3pm' to +256700123456 and +254700987654"*

Run:
```bash
python3 scripts/send_sms.py --to "+256700123456,+254700987654" --message "Meeting moved to 3pm"
```

The API charges per recipient. Surface the total cost back to the user.

### Sandbox testing

When testing the skill without using credits or sending real SMS:

```bash
AT_USERNAME=sandbox AT_API_KEY=<sandbox-key> AT_SENDER_ID=test \
  python3 scripts/send_sms.py --to "+256700123456" --message "Test" --sandbox
```

The sandbox endpoint accepts the call and returns a success response, but no SMS goes to the actual phone. AT_SENDER_ID is still required — sandbox doesn't validate it but the script does.

## Things to watch out for

- **Phone number format is strict.** AT requires E.164 (`+<country><number>`). Sending `0700123456` (Kenyan local format) returns an error. Always normalise to international format first.
- **Sender ID must be registered.** If you set `AT_SENDER_ID=DIGNITED` without registering that ID with your AT account, AT silently ignores it and the message either fails or goes out under a generic shortcode. Register sender IDs in the AT dashboard before relying on them — sender ID approval can take 24–72h.
- **Cost is per recipient, per segment.** A 200-char message to 100 people is 100 × 2 segments = 200 billable units. Budget before bulk sends.
- **Production keys vs sandbox keys are different.** A key from your sandbox account won't work against the production endpoint and vice versa. Sandbox `username` is always `sandbox`.
- **Don't echo the API key in any output.** The script intentionally never prints it. If you're debugging via curl, use `Authorization` masking.

## When this skill is the wrong tool

- **Long-form messages** (>1 SMS segment) — consider email or push notifications instead; SMS is per-segment expensive.
- **Two-way conversations** — AT supports inbound SMS but it requires webhook setup; that's a different skill.
- **Voice calls** — AT has a separate Voice API.
- **WhatsApp** — AT supports WhatsApp messaging via a separate channel; use that skill instead.
