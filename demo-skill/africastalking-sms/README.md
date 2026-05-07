# Demo skill: africastalking-sms

This is the **live demo skill** for the talk *"Designing Production-Ready Skills for AI Agents"* at Africa's Talking East Africa Hub on 2026-05-07.

## What it does

A Claude Code skill that takes a phone number and a message, then sends a real SMS via the [Africa's Talking](https://africastalking.com/) bulk SMS API. Reads credentials from environment variables (`AT_USERNAME`, `AT_API_KEY`) — never embeds them in the skill files.

## Why this skill, why this venue

- **Tangible end-to-end demo.** The audience sees the SMS arrive on a real phone in the room. You can't fake that.
- **Uses the venue's own product.** Africa's Talking host the event — showing their API integrated with an AI agent is a respectful nod and a real reference customer story.
- **Safe credential handling is a teaching point.** The skill doesn't embed the API key; the audience learns the right pattern.
- **Small enough to walk through end-to-end on stage.** Two files, ~150 lines, zero external dependencies.

## Files

```
africastalking-sms/
├── SKILL.md              # The skill definition — show this on stage
├── README.md             # This file (operator notes — not shown on stage)
└── scripts/
    └── send_sms.py       # Stdlib-only Python script — show this on stage
```

## Setup before the talk (15 min)

### 1. Install the skill into Claude Code

If you've already installed it at `~/.claude/skills/africastalking-sms/`, skip this step. Otherwise:

```bash
mkdir -p ~/.claude/skills/africastalking-sms/scripts
cp SKILL.md ~/.claude/skills/africastalking-sms/SKILL.md
cp scripts/send_sms.py ~/.claude/skills/africastalking-sms/scripts/send_sms.py
chmod +x ~/.claude/skills/africastalking-sms/scripts/send_sms.py
```

### 2. Set your AT credentials in your shell

For the live demo with real SMS delivery, use **production** credentials. In whatever terminal you'll run Claude Code from:

```bash
export AT_USERNAME="<your-AT-account-username>"
export AT_API_KEY="<your-production-API-key>"
```

To make these persistent across terminal sessions, put them in your `~/.zshrc` or `~/.bashrc`:

```bash
# Africa's Talking demo creds
export AT_USERNAME="dignited"   # or whatever your AT username is
export AT_API_KEY="atsk_..."     # never commit this anywhere
```

**Don't put them in a file inside this folder** — this folder might end up in a public repo or shared with attendees.

### 3. Verify the skill works (dry-run, no SMS sent)

```bash
AT_USERNAME=test AT_API_KEY=test \
  python3 ~/.claude/skills/africastalking-sms/scripts/send_sms.py \
  --to "+256700000000" --message "Test" --dry-run
```

Should output the request body with the api key masked as `***`. If you see this, the script is wired correctly.

### 4. Send a test SMS to your own phone (uses 1 credit)

```bash
python3 ~/.claude/skills/africastalking-sms/scripts/send_sms.py \
  --to "+256<your-number>" \
  --message "Test from agent-skills demo prep"
```

If your phone buzzes within ~10 seconds, the demo is ready.

If not, check:
- Phone number is in E.164 format (must start with `+`)
- `AT_USERNAME` matches your AT account (production, not "sandbox")
- `AT_API_KEY` is the production key from the AT dashboard
- AT account has credits (`account.africastalking.com` to top up)

## On stage — the demo flow (~5 min)

### Slide setup

Have these open in advance, all in your browser:
- Tab 1: `~/.claude/skills/africastalking-sms/SKILL.md` — viewable in your editor
- Tab 2: `~/.claude/skills/africastalking-sms/scripts/send_sms.py` — also in your editor
- Tab 3: A Claude Code session — terminal or claude.ai/code

### Step 1 — Show the SKILL.md (90 seconds)

Open the file. Walk through:
1. The frontmatter — `name`, `description`, `compatibility`. Point at `description` and say "this is what tells Claude when to invoke this skill."
2. Scroll down — show the "When to use" section, the env-var requirements, the example invocation.
3. **Highlight the line about not committing the API key.** Pause briefly: "this is the most common mistake people make with skills."

### Step 2 — Show the script (30 seconds)

Quick scroll through `send_sms.py`. Point at:
- `os.environ.get("AT_API_KEY")` — credentials from env, never embedded
- `urllib.request` — stdlib only, no SDK dependency
- The masking in `--dry-run` — never print the key

### Step 3 — Live invocation (90 seconds)

In the Claude Code terminal:

```
> Send an SMS to +256<volunteer-number-from-audience> saying
  "Hello from a Claude Code skill at Africa's Talking Kampala"
```

Watch the agent:
1. **Discover** the `africastalking-sms` skill (description matches "send an SMS")
2. **Activate** it (read SKILL.md)
3. **Execute** — invoke `python3 .../send_sms.py --to ... --message ...`
4. **Report** — show the JSON response with `accepted: 1`, message ID, cost

### Step 4 — Confirm receipt (60 seconds)

Volunteer holds up their phone with the SMS visible. Audience reaction.

(Or you SMS yourself, walk over to the projector with your phone, show the screen.)

### Step 5 — Recap the three layers (45 seconds)

Point back at the discovery → activation → execution diagram from earlier in the talk. The audience just watched all three happen.

## Backup plans

**If your laptop's wifi/internet is flaky:**
- Pre-record a short screencast (e.g. with OBS or asciinema) of the demo working at home, show that
- Switch to dignited.com pipeline as the demo (it works from cloud, not local)

**If the AT account has zero credit:**
- Top up at https://account.africastalking.com/ before the talk
- Or switch to `--sandbox` mode for the demo (works without credit, but no real SMS — you'll need to explain that)

**If the script errors live:**
- It's OK — show the JSON error output, explain that good skills surface errors clearly rather than failing silently
- Have a recorded successful run ready to fall back to

## Audience-volunteer SMS message ideas

Pick the message that matches the room's energy:

- *"Hello from a Claude Code skill at Africa's Talking Kampala 👋"*
- *"You just watched an AI agent send this SMS via an open-format skill"*
- *"agentskills.io — go build one"*
- *"Karibu Kampala, courtesy of agent skills"*

## Slide references

The slide deck has 4 slides dedicated to this demo (see `slides.md`):

- "Demo time" — what the audience will see
- "Demo: setup" — credentials + skill installation (mention briefly)
- "Demo: live" — the actual on-stage execution
- "What you'd build for your own use case" — leave-behind ideas

## After the talk

If attendees ask for the skill source: point them at `https://agentskills.io/` and tell them this skill will be on your blog within 48h. Don't share the API key. Each attendee creates their own AT account at africastalking.com (free tier exists).
