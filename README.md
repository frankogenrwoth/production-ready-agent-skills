# Designing Production-Ready Skills for AI Agents

Talk for Africa's Talking East Africa Hub · Kampala · 2026-05-07
[event page](https://community.africastalking.com/events/details/africas-talking-africas-talking-open-community-east-africa-hub-presents-designing-production-ready-skills-for-ai-agents/)

## Files in this folder

| File | What |
|---|---|
| `slides.md` | Marp-flavored markdown source. Edit this if you want to change content. |
| `slides.pptx` | PowerPoint export. Open in PowerPoint / Keynote / Google Slides / LibreOffice. |
| `slides.pdf` | PDF export. Use as backup if PPT doesn't render correctly on the venue laptop. |
| `README.md` | This file — speaker notes, demo prep, Q&A. |

## How to present

**Best path:** open `slides.pptx` directly in PowerPoint or Keynote on your laptop. Slide count: ~43.

**Alternative (Google Slides):** upload `slides.pptx` to Google Drive → right-click → Open with Google Slides → it auto-converts. The conversion is usually clean for Marp output.

**Web fallback:** if you have internet at the venue, you can render the markdown directly:
```bash
cd /home/oquidave/talks/agent-skills-2026-05-07
npx @marp-team/marp-cli slides.md --preview
```

## Talk structure (~38 min + Q&A)

| Time | Slides | Section |
|---|---|---|
| 0:00–2:00 | 1–4 | Intro + audience check |
| 2:00–5:00 | 5–8 | What's an agent / what's the problem |
| 5:00–11:00 | 9–14 | **What skills are** (how-to-guide framing) + what they're NOT + format |
| 11:00–15:00 | 15–18 | Anatomy + real example |
| 15:00–23:00 | 19–25 | Design principles + anti-patterns |
| 23:00–32:00 | 26–30 | **Demo (live)** |
| 32:00–37:00 | 31–37 | Practical next steps + marketplaces + resources |
| 37:00+ | 38–39 | Q&A / Thanks |

## Demo prep checklist (Africa's Talking SMS demo)

**Detailed prep guide:** `demo-skill/africastalking-sms/README.md`

**Quick checklist before the talk:**

- [ ] Skill installed at `~/.claude/skills/africastalking-sms/` ✓ (already done)
- [ ] `AT_USERNAME` set in your shell — `export AT_USERNAME="<your-AT-username>"`
- [ ] `AT_API_KEY` set in your shell — `export AT_API_KEY="atsk_..."`
- [ ] Test SMS to your own phone confirms delivery (uses ~1 credit)
- [ ] AT account has credits — top up at https://account.africastalking.com/ if needed
- [ ] Editor open with `~/.claude/skills/africastalking-sms/SKILL.md` and `scripts/send_sms.py`
- [ ] Claude Code session ready (terminal or claude.ai/code)
- [ ] A volunteer / specific phone number in mind for the live SMS

**Backup plan if AT API or wifi flaky:**
- Pre-record the demo (asciinema or screencast) — show the recording instead
- Or fall back to dignited pipeline demo (cloud-based, no local network needed):
  - Show `https://claude.ai/code/routines/trig_01SX2DUSJS8erZauqvgnPHh7`
  - Walk through the conversational digest → reply → drafts flow
  - Open one of the published articles (https://www.dignited.com/119506/... or 119507) as proof

## Key talking points (don't skip)

1. **Skills are a folder + SKILL.md** — say this multiple times. Simple framing students remember.
2. **Description is the most important field** — that's what the agent uses to decide. Bad description = skill never invoked.
3. **Progressive disclosure** — three stages. The 100-token discovery cost is the magic that makes "100 skills" feasible.
4. **Process over prose** — the most actionable principle. Show the bad-vs-good example slowly.
5. **Real production value** — emphasise this isn't theory. Two articles published this week from the pipeline.

## Common Q&A

**Q: Do skills work with all LLMs or only Claude?**
A: The format is open and now supported by 30+ products including Claude, GPT-based agents (OpenCode, Codex), Gemini CLI, Cursor, etc. Originally Anthropic, but it's open standard now.

**Q: How is this different from MCP (Model Context Protocol)?**
A: MCP is for **connecting** an agent to external **services** (a database, a calendar, an API). Skills are **instructions** that teach an agent **how to perform a task** — often using those MCP-connected services. Complementary, not competing.

**Q: How is this different from system prompts?**
A: System prompts are baked into the agent and apply to every conversation. Skills are **on-demand** — loaded only when relevant via the description match. So you can have many specialised skills without bloating every conversation.

**Q: Do I need to know Python?**
A: No. The minimal skill is just a `SKILL.md` with frontmatter and Markdown. Scripts are optional. You can write skills entirely in plain text.

**Q: Can skills call APIs / external services?**
A: Yes — through `scripts/` (e.g., a Python script using `requests`), or via MCP connectors the agent has, or via the agent's built-in tools. The skill instructs the agent on **when** and **how** to make the call.

**Q: Where do skills live? In my project repo? In my home directory?**
A: Both work. **Project-level** skills live at `.claude/skills/` (or equivalent for your agent) — they ship with the codebase, version-controlled. **User-level** skills live at `~/.claude/skills/` — available across all your projects on that machine. Use whichever scope fits.

**Q: Can I share my skills with my team?**
A: Yes. Commit them to git like any other code. Or publish to a marketplace — there are several emerging (claudemarketplaces.com, agentskills.io directory).

**Q: What's the biggest mistake beginners make?**
A: Writing essays instead of workflows. The skill reads like documentation — but agents need step-by-step instructions with checkpoints. Process over prose.

**Q: Will agents replace developers?**
A: No, but developers who use agents well will out-pace those who don't. Skills are how you teach agents your specific work. (Diplomatic answer that probably comes up.)

## Things to mention if running short on time

- Skip "Anti-rationalization" slide (advanced)
- Skip the second "common anti-pattern" slide
- Compress the 5 design principles into 2 slides

## Things to add if running long

- Walk through ALL the design principles with examples
- Show the actual Python script content (`fetch_feeds.py`)
- Discuss skill-creator (the meta-skill that helps you write skills)
- Demo the rewrite + publish step end-to-end (vs just the digest)

## After the talk

- Push slides to a public location (your blog, GitHub) and tweet the link
- Mention the dignited site as a real production reference
- Encourage attendees to start with a tiny single-purpose skill, not a mega one
