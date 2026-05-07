# africastalking-sms

A [Claude Code skill](https://code.claude.com/docs/en/skills) that sends SMS via the [Africa's Talking](https://africastalking.com/) bulk SMS API.

```
africastalking-sms/
├── SKILL.md          # Skill specification — what the agent reads
├── README.md         # This file — install + use
└── scripts/
    └── send_sms.py   # Stdlib-only Python; the agent invokes this
```

## What it does

- Sends one or more SMS messages via Africa's Talking
- Reads credentials from environment variables — never embeds them
- Uses Python's standard library only (no `requests`, no `africastalking` SDK)
- Returns structured JSON: per-recipient status code, cost, message ID
- Errors out clearly with actionable messages when something is missing

## Install

User-level (available across all your Claude Code sessions):

```bash
mkdir -p ~/.claude/skills/africastalking-sms/scripts
cp SKILL.md         ~/.claude/skills/africastalking-sms/SKILL.md
cp scripts/send_sms.py ~/.claude/skills/africastalking-sms/scripts/send_sms.py
chmod +x ~/.claude/skills/africastalking-sms/scripts/send_sms.py
```

Project-level (skill ships with a specific repo): copy to `<project-root>/.claude/skills/africastalking-sms/` instead.

## Set credentials

Three environment variables, all required:

```bash
export AT_USERNAME="<your-AT-username>"           # or 'sandbox' for testing
export AT_API_KEY="<your-production-api-key>"
export AT_SENDER_ID="<your-registered-sender-id>" # alphanumeric or shortcode
```

Get them from your [Africa's Talking dashboard](https://account.africastalking.com/). Add to `~/.zshrc` or `~/.bashrc` if you want them persistent across terminal sessions. **Never commit them to git.**

## Use

### Through Claude Code (recommended)

In any Claude Code session — terminal, [claude.ai/code](https://claude.ai/code), or another compatible agent — say something like:

> Send an SMS to +256787624334 saying "Server backups completed at 03:00 UTC"

Claude reads `SKILL.md`, decides the skill applies, and runs the script. You get back delivery status in plain language.

### Direct invocation

You can also call the script without an agent:

```bash
# Single recipient
python3 scripts/send_sms.py \
  --to "+256787624334" \
  --message "Hello from the script"

# Multiple recipients (comma-separated)
python3 scripts/send_sms.py \
  --to "+256700123456,+254700987654,+233200111222" \
  --message "Meeting moved to 3pm"

# Dry-run — prints the request without sending (api key is masked)
python3 scripts/send_sms.py --to "+256700000000" --message "Test" --dry-run

# Sandbox endpoint (no real SMS, no credits used)
AT_USERNAME=sandbox python3 scripts/send_sms.py \
  --to "+256700000000" --message "Test" --sandbox
```

## Flags

| Flag | What it does |
|---|---|
| `--to` | Recipient phone number(s) in E.164 format (`+<country><number>`). Comma-separated for multiple. **Required.** |
| `--message` | The SMS body. **Required.** |
| `--sender-id` | Override `AT_SENDER_ID` for a single call |
| `--sandbox` | POST to AT's sandbox endpoint instead of production |
| `--enqueue` | Tell AT to queue the request and return immediately (useful for bulk) |
| `--dry-run` | Print the request that would be sent and exit |

## Exit codes

| Code | Meaning |
|---|---|
| 0 | At least one recipient was accepted by AT |
| 1 | Credential or input validation failed |
| 2 | HTTP / API error from AT |

## Output format

Successful run, single recipient:

```json
{
  "ok": true,
  "endpoint": "production",
  "summary": "Sent to 1/1 Total Cost: UGX 27.0000",
  "recipients": 1,
  "accepted": 1,
  "details": [
    {
      "number": "+256787624334",
      "status": "Success",
      "status_code": 100,
      "cost": "UGX 27.0000",
      "message_id": "ATXid_846b6de8a47611c792ca6a32931e8a73"
    }
  ]
}
```

`status_code` follows [AT's status code reference](https://developers.africastalking.com/docs/sms/sending/status_codes). The script treats `100` (Processed), `101` (Sent), and `102` (Queued) as success.

## Things to watch for

- **E.164 format is strict.** AT requires `+<country><number>` — `0700123456` (local format) is rejected. Always normalise first.
- **Sender ID approval takes 24–72 hours.** Your `AT_SENDER_ID` must be registered and approved by AT (and Uganda's regulator) before it's used. Until then, AT may silently fall back to a generic shortcode or reject the message.
- **Cost is per recipient, per segment.** A 200-character message to 100 people = 100 × 2 segments = 200 billable units.
- **Production keys ≠ sandbox keys.** A production key won't work against the sandbox endpoint and vice versa. The sandbox username is always `sandbox`.

## When this skill is the wrong tool

- **Long-form messages** (multi-segment) — consider email or push notifications; SMS is per-segment expensive.
- **Two-way conversations** — AT supports inbound SMS but it requires webhook setup; that's a separate skill.
- **Voice calls** — AT has a separate Voice API.
- **WhatsApp** — AT has a separate WhatsApp channel.

## License

MIT.
