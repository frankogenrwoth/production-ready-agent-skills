# Production-Ready Agent Skills

Slides and a working demo skill from the talk *"Designing Production-Ready Skills for AI Agents"* — given at the **Africa's Talking East Africa Hub** in Kampala on 2026-05-07. [Event page](https://community.africastalking.com/events/details/africas-talking-africas-talking-open-community-east-africa-hub-presents-designing-production-ready-skills-for-ai-agents/).

If you weren't there: this repo is a self-contained introduction to the **agent skill** format — what it is, why it matters, and what makes a skill production-grade — anchored to a concrete working example: a Claude Code skill that sends real SMS via the [Africa's Talking](https://africastalking.com/) bulk SMS API.

## What's an agent skill?

In plain terms, an agent skill is a how-to guide written for an AI agent. Instead of teaching *you* how to do something, it teaches the *agent* how. A skill is just a folder with a `SKILL.md` (the instructions, plus YAML frontmatter that tells the agent *when* to use it) and optionally a few scripts the agent can run.

The format is open and works across many agents — Claude Code, Cursor, Codex, Gemini CLI, OpenCode, and others. See [agentskills.io](https://agentskills.io) for the spec.

## What's in this repo

| Path | What |
|---|---|
| `slides.md` | Marp-flavored markdown source of the talk deck |
| `slides.pptx` | PowerPoint export — open in PowerPoint / Keynote / Google Slides / LibreOffice |
| `slides.pdf` | PDF export — backup viewing format |
| `demo-skill/africastalking-sms/` | A working Claude Code skill that sends SMS via Africa's Talking |

## The demo skill: `africastalking-sms`

The `demo-skill/africastalking-sms/` folder is a complete skill you can install and use today. It:

- Sends one or more SMS messages via Africa's Talking's bulk SMS API
- Reads credentials from environment variables — never embeds them in the skill files
- Uses Python's standard library only — no `requests`, no SDK, no install step beyond Python 3
- Returns structured JSON (per-recipient status code, cost, message ID)
- Errors out clearly when credentials or sender ID are missing

### Install

```bash
# User-level: available across all your projects on this machine
mkdir -p ~/.claude/skills/africastalking-sms/scripts
cp demo-skill/africastalking-sms/SKILL.md \
   ~/.claude/skills/africastalking-sms/SKILL.md
cp demo-skill/africastalking-sms/scripts/send_sms.py \
   ~/.claude/skills/africastalking-sms/scripts/send_sms.py
chmod +x ~/.claude/skills/africastalking-sms/scripts/send_sms.py
```

For a project-level install (skill ships with a specific codebase), copy to `<project-root>/.claude/skills/africastalking-sms/` instead.

### Set credentials

Get them from your [Africa's Talking dashboard](https://account.africastalking.com/), then set in your shell:

```bash
export AT_USERNAME="<your-AT-username>"
export AT_API_KEY="<your-production-api-key>"
export AT_SENDER_ID="<your-registered-sender-id>"   # alphanumeric or shortcode
```

Add them to `~/.zshrc` or `~/.bashrc` if you want them persistent. **Don't commit them to git, ever.**

### Use it

In any Claude Code session — terminal or [claude.ai/code](https://claude.ai/code) — say something like:

> Send an SMS to +256787624334 saying "Server backups completed at 03:00 UTC"

Claude reads the skill's description, decides it's relevant, loads the full instructions, and runs the script. You get back delivery status in plain language.

You can also call the script directly, no agent involved:

```bash
python3 ~/.claude/skills/africastalking-sms/scripts/send_sms.py \
  --to "+256787624334" \
  --message "Hello from the script"
```

For full skill specification — all flags, sandbox testing, multi-recipient bulk sends, per-status-code semantics, and gotchas — see [`demo-skill/africastalking-sms/SKILL.md`](demo-skill/africastalking-sms/SKILL.md).

## Slides

The deck is written in [Marp](https://marp.app/). Read `slides.md` for the source; open `slides.pptx` or `slides.pdf` for a rendered version. To re-render after editing the markdown:

```bash
npx @marp-team/marp-cli slides.md --pdf  --output slides.pdf  --allow-local-files
npx @marp-team/marp-cli slides.md --pptx --output slides.pptx --allow-local-files
```

## FAQ

**How is this different from MCP (Model Context Protocol)?**
MCP connects an agent to external *services* (a database, a calendar, an API). Skills are *instructions* that teach an agent how to perform a task — often using those MCP-connected services. Complementary, not competing.

**How is this different from a system prompt?**
System prompts apply to every conversation and are baked into the agent. Skills are loaded on-demand — only when their `description` matches what the user is asking — so you can have many specialised skills without bloating every conversation's context.

**Do skills only work with Claude?**
The format is open and supported by many products including Claude Code, Cursor, Codex, Gemini CLI, OpenCode, and others. Originally Anthropic-led; now adopted broadly.

**Do I need to write Python to make a skill?**
No. The minimum is a `SKILL.md` file with frontmatter and Markdown. Scripts are optional. Some skills are entirely plain text — they just instruct the agent how to think about a task.

**Can skills call external APIs?**
Yes — three ways: a script in the skill's `scripts/` folder (any language); an MCP connector the agent already has; or the agent's built-in tools (Bash, WebFetch, etc.). The skill tells the agent *when* and *how*.

**Where do skills live on disk?**
Two scopes: `~/.claude/skills/<name>/` for user-level (across all projects on your machine), or `<project-root>/.claude/skills/<name>/` for project-level (ships with the codebase). Either works; pick whichever fits.

**How do I share a skill with a team?**
Commit it to git like any other code. Or publish to a marketplace — see [skills.sh](https://skills.sh), [claudemarketplaces.com/skills](https://claudemarketplaces.com/skills), or the [agentskills.io](https://agentskills.io) directory.

**What's the most common beginner mistake?**
Writing the skill like documentation when it should be a workflow. Agents follow step-by-step instructions with checkpoints, not paragraphs of prose.

## Speaker

**David Okwii** — Lead Software Developer at Serve Digital, Kampala. Also runs [dignited.com](https://dignited.com), Uganda's tech blog (since 2013), where he's been building production AI agent pipelines.

- 🐦 [@oquidave](https://twitter.com/oquidave)
- 📧 oquidave@gmail.com

## Resources from the talk

- [agentskills.io](https://agentskills.io) — the open spec for the skill format
- [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) — Claude Code skill docs
- [Addy Osmani on agent skills](https://addyosmani.com/blog/agent-skills/) — design principles
- [skills.sh](https://skills.sh) · [claudemarketplaces.com/skills](https://claudemarketplaces.com/skills) — skill marketplaces
- [github.com/anthropics/skills](https://github.com/anthropics/skills) — Anthropic's official skills
- [Africa's Talking SMS API docs](https://developers.africastalking.com/docs/sms/overview) — used by the demo skill

## License

Skill code (`demo-skill/`) is MIT — feel free to fork, adapt, and ship.
Slides are CC-BY 4.0 — remix freely with attribution.
