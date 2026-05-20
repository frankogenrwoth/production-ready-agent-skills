---
name: twillio-whatsapp
description: Send a WhatsApp message through Twilio using the local Python helper. Use whenever the user wants to message a person on WhatsApp, send a notification, deliver a short update, or any phrasing that involves sending text through WhatsApp.
license: MIT
compatibility: Requires Python 3, twilio, and python-dotenv. Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN before sending.
metadata:
  version: "1.0"
---

# Twilio WhatsApp

A skill for sending a WhatsApp message through the local Twilio helper in [scripts/twillio_whatsapp.py](scripts/twillio_whatsapp.py).

## When to use

Trigger this skill when the user asks to:

- "Send a WhatsApp message to +123… saying …"
- "Text someone on WhatsApp"
- "Send a quick WhatsApp update"
- "Notify the team on WhatsApp"
- Anything else where the goal is delivering a short message through WhatsApp

If the user wants email, SMS, or a long document, this is the wrong skill.

## Required environment variables

Two env vars must be set before invoking the helper:

| Variable | What it is | Example |
|---|---|---|
| `TWILIO_ACCOUNT_SID` | Your Twilio account SID | `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `TWILIO_AUTH_TOKEN` | Your Twilio auth token | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |

The script loads these from the environment with `python-dotenv`. Do not place secrets in this file.

## How to use

The helper is a Python function, not a CLI. Call it from Python like this:

```python
from skills.twillio_whatsapp import send_whatsapp_message

message_sid = send_whatsapp_message(
    "whatsapp:+1234567890",
    "Hello from a Copilot skill"
)
print(message_sid)
```

The recipient number must use Twilio's WhatsApp format: `whatsapp:+<countrycode><number>`.

## Workflow

1. **Confirm the recipient number.** It must include `whatsapp:+` and the international country code.
2. **Confirm the message content.** If it contains sensitive information, echo it back before sending.
3. **Call the helper** in [scripts/twillio_whatsapp.py](scripts/twillio_whatsapp.py) by importing `send_whatsapp_message`.
4. **Read the return value.** The helper returns the Twilio message SID.
5. **Report success** to the user with the message SID and the recipient number.

## Example

User: *"Send WhatsApp message to +256700123456 saying 'Meeting starts in 10 minutes'"*

Run:

```python
from skills.twillio_whatsapp import send_whatsapp_message

sid = send_whatsapp_message(
    "whatsapp:+256700123456",
    "Meeting starts in 10 minutes"
)
print(sid)
```

## Things to watch out for

- **The helper currently uses the Twilio WhatsApp sandbox sender.** The sender number is hardcoded in [scripts/twillio_whatsapp.py](scripts/twillio_whatsapp.py), so the recipient must be joined to the sandbox or otherwise eligible to receive sandbox messages.
- **The destination format is strict.** Passing `+256700123456` without the `whatsapp:` prefix will not match the helper's expected input.
- **Missing credentials will fail immediately.** If `TWILIO_ACCOUNT_SID` or `TWILIO_AUTH_TOKEN` is empty, Twilio client creation will fail.
- **This skill sends text only.** It does not attach files, images, or interactive WhatsApp templates.

## When this skill is the wrong tool

- **Bulk messaging** — use a dedicated broadcast workflow instead.
- **Production WhatsApp automation** — you may need approved senders, templates, or a different Twilio configuration.
- **Two-way chatbot handling** — inbound webhooks and conversation state belong in a different skill.
