#!/usr/bin/env python3
"""Write sources.json, sources.csv, and js/claims.js from the ledger below."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CLAIMS = [
  {
    "id": "C01", "cluster": "grok",
    "claim": "Grok Bot is described by xAI as a proactive teammate with a real cloud computer (browser, filesystem, terminal), chat plus voice, and custom tooling through any MCP server or API.",
    "url": "https://docs.x.ai/grok-bot/overview",
    "source_title": "Grok Bot overview",
    "author": "xAI", "date": "undated page, fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "Product documentation. Not an independent customer study."
  },
  {
    "id": "C02", "cluster": "grok",
    "claim": "xAI's overview says multiple Bots can split work and hand it off: one routine pulls numbers, another drafts, a third reviews, then a person approves.",
    "url": "https://docs.x.ai/grok-bot/overview",
    "source_title": "Grok Bot overview",
    "author": "xAI", "date": "undated page, fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "Vendor scenario, not a named customer's books."
  },
  {
    "id": "C03", "cluster": "grok",
    "claim": "xAI says you can walk a Bot through a task once, save the steps as a skill, and rerun them as a routine on a schedule.",
    "url": "https://docs.x.ai/grok-bot/overview",
    "source_title": "Grok Bot overview",
    "author": "xAI", "date": "undated page, fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": ""
  },
  {
    "id": "C04", "cluster": "grok",
    "claim": "The same overview publishes connector scenarios: Gmail drafts left unsent, a Sunday-evening calendar plan, Granola notes turned into a Slack post after approval, Slack mention drafts, and Friday Notion project updates after approval.",
    "url": "https://docs.x.ai/grok-bot/overview",
    "source_title": "Grok Bot overview",
    "author": "xAI", "date": "undated page, fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "These are official examples, not audited case studies."
  },
  {
    "id": "C05", "cluster": "grok",
    "claim": "xAI lists prebuilt bots named Overheard, Tradbot, Meeting Recap Deck, and Pitch Deck Coach, including Overheard's rule that it never posts on your behalf.",
    "url": "https://docs.x.ai/grok-bot/overview",
    "source_title": "Grok Bot overview",
    "author": "xAI", "date": "undated page, fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": ""
  },
  {
    "id": "C06", "cluster": "grok",
    "claim": "Grok Bot changelog lists v1.2.3 on 18 Nov 2026 (also covering 1.2.1 and 1.2.2). Connector pages can set each tool to Always allow, Auto-review, Needs approval, or Blocked.",
    "url": "https://x.ai/changelog/bot",
    "source_title": "Grok Bot changelog",
    "author": "xAI", "date": "2026-11-18",
    "confidence": "high", "independence": "primary",
    "notes": ""
  },
  {
    "id": "C07", "cluster": "grok",
    "claim": "In that 1.2.3 changelog, a routine that loses a connector sign-in skips scheduled runs until you sign back in, and routines can read the earlier conversation in the chat they run in.",
    "url": "https://x.ai/changelog/bot",
    "source_title": "Grok Bot changelog",
    "author": "xAI", "date": "2026-11-18",
    "confidence": "high", "independence": "primary",
    "notes": ""
  },
  {
    "id": "C08", "cluster": "grok",
    "claim": "The 1.2.3 changelog says that for a site with a connector, the Bot uses the connector or shows its connect card before opening the browser, and that the Bot keeps separate memories for people and organizations, your profile, standing instructions, and projects.",
    "url": "https://x.ai/changelog/bot",
    "source_title": "Grok Bot changelog",
    "author": "xAI", "date": "2026-11-18",
    "confidence": "high", "independence": "primary",
    "notes": "Ctrl+K search finding Bots and Pages is also in this changelog. That is the only Pages behavior verified here."
  },
  {
    "id": "C09", "cluster": "grok",
    "claim": "xAI's skills announcement says Skills are live on Grok 4.3 across grok.com, iOS, and Android; built-in skills can be overridden; a skill can be created by describing it, uploading a file, or asking Grok to save what it learned.",
    "url": "https://x.ai/news/grok-skills",
    "source_title": "Skills in web, iOS, and Android",
    "author": "xAI", "date": "undated page, fetched 2026-11-20",
    "confidence": "medium", "independence": "primary",
    "notes": "The page does not show a publication date. It does not by itself prove Grok 4.3 is the newest model. See gap G01."
  },
  {
    "id": "C10", "cluster": "grok",
    "claim": "The skills page publishes four example prompts for decks, invoices, budgets, and PDF reports. They are xAI's examples, not a customer's prompts.",
    "url": "https://x.ai/news/grok-skills",
    "source_title": "Skills in web, iOS, and Android",
    "author": "xAI", "date": "undated page, fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "Quoted in the prompt vault."
  },
  {
    "id": "C11", "cluster": "claude",
    "claim": "On 23 Oct 2026 Anthropic opened a research preview of Claude Duet, a separate app on iOS, Android, and claude.ai, for US Pro, Max, and Ultra subscribers via a waitlist, sharing the plan's usage limits.",
    "url": "https://claude.com/resources/articles/claude-duet",
    "source_title": "Introducing Claude Duet",
    "author": "Anthropic", "date": "2026-10-23",
    "confidence": "high", "independence": "primary",
    "notes": "TechCrunch's 22 Oct 2026 piece is an echo of this announcement, not a second origin."
  },
  {
    "id": "C12", "cluster": "claude",
    "claim": "Anthropic says Claude Duet is designed around Claude Opus 5.5, sends a morning brief, runs on a virtual machine with its own browser, checks connected accounts every few hours, and asks before it sends a message, pays, signs, or deletes. Trading securities and moving money between accounts stay off-limits even with approval.",
    "url": "https://claude.com/resources/articles/claude-duet",
    "source_title": "Introducing Claude Duet",
    "author": "Anthropic", "date": "2026-10-23",
    "confidence": "high", "independence": "primary",
    "notes": ""
  },
  {
    "id": "C13", "cluster": "claude",
    "claim": "Anthropic says Duet carries over memory, skills, and connected apps, and can use the Claude Marketplace's connectors and plugins, which the announcement counts as over 6,000. The preview cannot show you its browser.",
    "url": "https://claude.com/resources/articles/claude-duet",
    "source_title": "Introducing Claude Duet",
    "author": "Anthropic", "date": "2026-10-23",
    "confidence": "high", "independence": "primary",
    "notes": "Connector count is Anthropic's figure."
  },
  {
    "id": "C14", "cluster": "claude",
    "claim": "Anthropic attributes early uses to named people: Boris Cherny talks through a mental to-do list with Duet on walks; Chelsea Larsson hands it her to-do list before leaving for her kids; Karan Ahuja uses it to schedule interviews, partner on prototypes, and ship code.",
    "url": "https://claude.com/resources/articles/claude-duet",
    "source_title": "Introducing Claude Duet",
    "author": "Anthropic", "date": "2026-10-23",
    "confidence": "medium", "independence": "primary",
    "notes": "Primary as Anthropic's account of its own staff. Not an independent interview. Workflows are one sentence each."
  },
  {
    "id": "C15", "cluster": "claude",
    "claim": "Anthropic quotes three early-access business users: Jess Provencher (Pro Homes) on a morning rundown that flagged a showing on the wrong day; Amin Ebrahimi (Shahs of Kabob, about 110 employees) on accounting, support, marketing, and invoices store by store; Mya Dalton on a pre-call brief and an offer to move a call that sat before a flight.",
    "url": "https://claude.com/resources/articles/claude-duet",
    "source_title": "Introducing Claude Duet",
    "author": "Anthropic", "date": "2026-10-23",
    "confidence": "medium", "independence": "primary",
    "notes": "Selected testimonials in a launch post. No books, prompts, or screenshots were published with them."
  },
  {
    "id": "C16", "cluster": "claude",
    "claim": "Anthropic's help center says that during the preview you cannot choose a model (Duet runs on Claude Opus 5.5), it is not on Team or Enterprise yet, finished work appears in the Make tab, it cannot see all projects or the files on your computer, and Personal Finance is unavailable.",
    "url": "https://support.claude.com/en/articles/17631495-get-started-with-claude-duet",
    "source_title": "Get started with Claude Duet",
    "author": "Anthropic Help Center", "date": "fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "Read from the help-center extract returned with search, then the URL was link-checked."
  },
  {
    "id": "C17", "cluster": "claude",
    "claim": "Claude Code's best-practices page separates non-deterministic instructions (prompt, CLAUDE.md, skills) from deterministic ones (hooks, deny rules, sandbox, managed settings). It says a line you keep emphasizing in CLAUDE.md belongs in a hook.",
    "url": "https://code.claude.com/docs/en/best-practices",
    "source_title": "Best practices for Claude Code",
    "author": "Anthropic", "date": "fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "Page has no visible version stamp."
  },
  {
    "id": "C18", "cluster": "claude",
    "claim": "The same page says skill bodies load only when the task calls for them, while CLAUDE.md weighs on every session. Subagents help for parallel work, for keeping noisy output out of the main context, and for a reviewer that has not seen how the code was written. Their requests count toward the same usage.",
    "url": "https://code.claude.com/docs/en/best-practices",
    "source_title": "Best practices for Claude Code",
    "author": "Anthropic", "date": "fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": ""
  },
  {
    "id": "C19", "cluster": "claude",
    "claim": "Anthropic's documented prompt rewrites replace 'fix the login bug' with a symptom, a path, and a failing test, and replace 'add a calendar widget' with a pattern file and a no-new-libraries constraint. It also shows a 'be ambitious' scope line for a settings page.",
    "url": "https://code.claude.com/docs/en/best-practices",
    "source_title": "Best practices for Claude Code",
    "author": "Anthropic", "date": "fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "Official examples, not a user's production prompt."
  },
  {
    "id": "C20", "cluster": "claude",
    "claim": "The skills docs say Claude Code skills follow the Agent Skills open standard, and context: fork runs a skill in a subagent. The subagents docs say each subagent has its own context, tool access, and permissions, and that description text occupies context so it should stay short.",
    "url": "https://code.claude.com/docs/en/skills",
    "source_title": "Extend Claude with skills",
    "author": "Anthropic", "date": "fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "Subagent half also supported by https://code.claude.com/docs/en/sub-agents, fetched the same day."
  },
  {
    "id": "C21", "cluster": "claude",
    "claim": "Hooks can be shell commands, HTTP endpoints, MCP tool calls, prompts, or agents. Prompt and agent hooks are not deterministic. Command, HTTP, or mcp_tool hooks with onFailure block are the enforcement path. Stop hooks can be the definition of done.",
    "url": "https://code.claude.com/docs/en/best-practices",
    "source_title": "Best practices for Claude Code",
    "author": "Anthropic", "date": "fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "Event catalog is in https://code.claude.com/docs/en/hooks, fetched the same day."
  },
  {
    "id": "C22", "cluster": "claude",
    "claim": "On 2 Jan 2026 Boris Cherny posted that he ran five Claudes in local terminal tabs and five to ten on claude.ai/code, started PR work in Plan mode, then switched to auto-accept edits, used Opus 4.5 with thinking, kept a shared CLAUDE.md he described as 2.5k tokens, used slash commands and subagents such as code-simplifier and verify-app, formatted with a PostToolUse hook, avoided --dangerously-skip-permissions outside a sandbox, and had Claude test claude.ai/code changes with the Claude Chrome extension.",
    "url": "https://threadreaderapp.com/scrolly/2007179832300581177",
    "source_title": "Thread mirror of @bcherny",
    "author": "Boris Cherny", "date": "2026-01-02",
    "confidence": "medium", "independence": "primary",
    "notes": "Date is the snowflake timestamp of status 2007179832300581177. The mirror is not the X permalink. InfoQ's 2026-01 writeup echoes this thread. The model he named that day is Opus 4.5, which is not the Oct 2026 Duet model."
  },
  {
    "id": "C23", "cluster": "gemini",
    "claim": "Google's Antigravity changelog for 18 Nov 2026 says Gemini 4 Neon is available on Google AI Ultra, Google AI Pro, and Gemini Enterprise, is the default if you have not chosen a model, has four thinking levels, and Orchestrator (Neon) plans with Gemini 4 Neon and implements with Gemini 4 Hydrogen.",
    "url": "https://antigravity.google/docs/changelog/",
    "source_title": "Google Antigravity changelog",
    "author": "Google Antigravity", "date": "2026-11-18",
    "confidence": "high", "independence": "primary",
    "notes": ""
  },
  {
    "id": "C24", "cluster": "gemini",
    "claim": "Antigravity App v2.33.0 (17 Nov 2026) adds SSH connections to a remote 64-bit Linux machine, live GitHub pull-request status pills, and opens /swarm plus UI plugin panels to business and enterprise accounts when an admin allows them.",
    "url": "https://antigravity.google/docs/changelog/",
    "source_title": "Google Antigravity changelog",
    "author": "Google Antigravity", "date": "2026-11-17",
    "confidence": "high", "independence": "primary",
    "notes": ""
  },
  {
    "id": "C25", "cluster": "gemini",
    "claim": "App v2.32.0 (13 Nov 2026) adds Dynamic Workflows: agents orchestrate parallel subagents and multi-step tasks in Python using the runtime bundled with the app. v2.32.2 (16 Nov 2026) adds multi-turn /btw side questions with read-only tools.",
    "url": "https://antigravity.google/docs/changelog/",
    "source_title": "Google Antigravity changelog",
    "author": "Google Antigravity", "date": "2026-11-13",
    "confidence": "high", "independence": "primary",
    "notes": ""
  },
  {
    "id": "C26", "cluster": "gemini",
    "claim": "The 12 Nov 2026 changelog entry says Gemini 4 Hydrogen is for fast coding and agentic execution across four reasoning effort levels, alongside Orchestrator for dynamic multi-model planning and execution with Gemini 4 Carbon. The 11 Nov 2026 note adds Carbon to the model selector for Google Cloud application-default credentials.",
    "url": "https://antigravity.google/docs/changelog/",
    "source_title": "Google Antigravity changelog",
    "author": "Google Antigravity", "date": "2026-11-12",
    "confidence": "high", "independence": "primary",
    "notes": "A full consumer-plan matrix for Carbon was not extracted. See gap G04."
  },
  {
    "id": "C27", "cluster": "gemini",
    "claim": "App v2.31.0 (9 Nov 2026) says you can use /swarm to coordinate multiple subagents over a message board to complete long-horizon tasks. The changelog text around Carbon calls Carbon the strongest model for long-horizon software engineering, knowledge work, scientific discovery, and cybersecurity.",
    "url": "https://antigravity.google/docs/changelog/",
    "source_title": "Google Antigravity changelog",
    "author": "Google Antigravity", "date": "2026-11-09",
    "confidence": "high", "independence": "primary",
    "notes": "Benchmark scores on the Neon blog were not used; that post was not fetched in full."
  },
  {
    "id": "C28", "cluster": "codex",
    "claim": "OpenAI introduced dots on 29 Sep 2026 and on 3 Nov 2026 added GPT-6.1 Terra to the models that power them. The launch post says dots were powered by GPT-6 Astra, have a cloud computer and browser, connect through plugins to over 4,000 apps, and can be reached in ChatGPT, Slack, and Teams.",
    "url": "https://openai.com/index/introducing-dots/",
    "source_title": "Introducing dots",
    "author": "OpenAI", "date": "2026-09-29",
    "confidence": "high", "independence": "primary",
    "notes": "Terra update date is in the same post."
  },
  {
    "id": "C29", "cluster": "codex",
    "claim": "OpenAI says a dot can delegate tasks to Codex or ChatGPT Work. Conversations with the dot do not count toward ChatGPT usage limits; those delegated tasks count as usual. Proactive research uses read-only tools. Custom Rules and auto-review decide what can proceed. Some actions, such as changing a password, always stay with the person.",
    "url": "https://openai.com/index/introducing-dots/",
    "source_title": "Introducing dots",
    "author": "OpenAI", "date": "2026-09-29",
    "confidence": "high", "independence": "primary",
    "notes": "Learn.chatgpt.com docs echo the product split between Chat, ChatGPT Work, Codex, and a dot."
  },
  {
    "id": "C30", "cluster": "codex",
    "claim": "The dots launch says rollout started for Pro and Business Premium in eligible markets, with Enterprise including Edu and Healthcare as a beta an admin enables. The first dot is included in Pro or Business Premium. Specialist dots, with their own identity, were a preview, including pilots OpenAI says covered procurement, invoices, email marketing, support, and contracting.",
    "url": "https://openai.com/index/introducing-dots/",
    "source_title": "Introducing dots",
    "author": "OpenAI", "date": "2026-09-29",
    "confidence": "high", "independence": "primary",
    "notes": "Learn docs later describe a Nov 18 2026 enterprise default-on change. That later sentence was seen in search highlights of learn.chatgpt.com/docs/dots and was not re-fetched as a full page. It is not a separate claim here."
  },
  {
    "id": "C31", "cluster": "codex",
    "claim": "OpenAI's own launch anecdotes: inside OpenAI, a bug appears in Slack and dots start investigating; a design becomes a working app; an unnamed early tester's dot prepared an invoice after noticing a missed invoice, and sent it after approval.",
    "url": "https://openai.com/index/introducing-dots/",
    "source_title": "Introducing dots",
    "author": "OpenAI", "date": "2026-09-29",
    "confidence": "low", "independence": "primary",
    "notes": "Primary as OpenAI's marketing anecdote. No name, repo, or artifact. Do not treat as an audited workflow."
  },
  {
    "id": "C32", "cluster": "codex",
    "claim": "The ChatGPT and Codex changelog entry dated 2026-11-20, and the GitHub release rust-v0.171.0 published 2026-11-20, say Codex CLI 0.171.0 adds GPT-6.2 Sol and Astra to the model catalog with Sol as the default catalog selection, turns on the TUI workspace by default, adds codex exec --remote, and adds /rc and /remote.",
    "url": "https://github.com/openai/codex/releases/tag/rust-v0.171.0",
    "source_title": "Codex rust-v0.171.0",
    "author": "OpenAI", "date": "2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "Same text is on https://learn.chatgpt.com/docs/changelog. One origin."
  },
  {
    "id": "C33", "cluster": "codex",
    "claim": "Mert Özen's 15 Nov 2026 post, which he says was checked against OpenAI's docs for Codex CLI 0.169.0, describes an AGENTS.md chain: global file, then one file per directory from the repo root to the working directory, closer file later, default project_doc_max_bytes of 32 KiB. Skills are SKILL.md folders discovered from .agents/skills and ~/.agents/skills; the model first sees name, description, and path, budgeted by default at 2% of the context window.",
    "url": "https://www.mertozen.com/en/blog/openai-codex-agents-md-config-toml-skills",
    "source_title": "Teaching Codex Your Project",
    "author": "Mert Özen", "date": "2026-11-15",
    "confidence": "medium", "independence": "secondary",
    "notes": "Secondary walkthrough of official docs. His sample config.toml is his example, not an OpenAI template. Official AGENTS.md page was not re-fetched in this pass."
  },
  {
    "id": "C34", "cluster": "codex",
    "claim": "GitHub user tibo-openai, whose profile name is Thibault Sottiaux, merged pull request 5353 in openai/codex on 19 Oct 2025, adding an AGENTS.md discovery guide.",
    "url": "https://github.com/openai/codex/pull/5353",
    "source_title": "docs: add AGENTS.md discovery guide",
    "author": "Thibault Sottiaux", "date": "2025-10-19",
    "confidence": "high", "independence": "primary",
    "notes": "Older than the Nov 2025-Nov 2026 window. Profile name checked via the GitHub API on 2026-11-20. Job title was not on the profile."
  },
  {
    "id": "C35", "cluster": "muse",
    "claim": "On 5 Aug 2026 Meta released Muse Code (beta), a terminal coding agent powered by Muse Spark 1.2. The install line in that post is curl -fsSL https://dev.meta.ai/install.sh | bash. Meta describes persistent async background agents, a local event log that is replay-exact after a crash, and bundled skills /plan, /grill, and /goal.",
    "url": "https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2",
    "source_title": "Introducing Muse Code and Muse Spark 1.2",
    "author": "Meta AI Research", "date": "2026-08-05",
    "confidence": "high", "independence": "primary",
    "notes": "Reuters's same-day article echoes this post."
  },
  {
    "id": "C36", "cluster": "muse",
    "claim": "Meta says Muse Spark 1.2 was co-trained with Muse Code, including rejection-sampled harness trajectories and recipe work for goals, compaction, and subagents, and that a kernel-optimization case study ran more than 1,000 tool calls for up to 24 hours on NVIDIA Hopper KDA and MLA kernels.",
    "url": "https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2",
    "source_title": "Introducing Muse Code and Muse Spark 1.2",
    "author": "Meta AI Research", "date": "2026-08-05",
    "confidence": "medium", "independence": "primary",
    "notes": "Meta's own case study. The linked evaluation report was not fetched."
  },
  {
    "id": "C37", "cluster": "muse",
    "claim": "Muse Code docs say the default model string is muse-spark-1.2, first run asks whether to trust the workspace, headless mode is muse exec, CI auth is META_API_KEY, workflows are not on every build, and session messaging is unavailable on Windows. muse serve exposes a session protocol; the TypeScript SDK is npm install @muse-code/sdk.",
    "url": "https://dev.meta.ai/docs/muse-code",
    "source_title": "Muse Code docs",
    "author": "Meta", "date": "fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "Docs still name 1.2 as the default while the pricing page also lists 1.3. See C38 and gap G05."
  },
  {
    "id": "C38", "cluster": "muse",
    "claim": "Meta's pricing page lists muse-spark-1.3, 1.2, and 1.1. Standard mode is $0.15 cached input, $1.25 input, and $4.25 output per 1M tokens. Contributor mode is $0.002, $0.10, and $0.20. Contributor mode is permission for Meta to use prompts, code, files, context, and responses to train future models. Muse Code subscriptions default to Contributor mode. Muse Wonder standard pricing on the same page is $0.20 cached, $4 input, $20 output, with no Contributor mode.",
    "url": "https://dev.meta.ai/docs/pricing-rate-limits",
    "source_title": "Pricing and rate limits",
    "author": "Meta", "date": "fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "Parsed from the rendered pricing page text on 2026-11-20."
  },
  {
    "id": "C39", "cluster": "mcp",
    "claim": "The MCP specification 2026-07-28, announced by David Soria Parra and Den Delimarsky, makes the protocol core stateless, retires the initialize handshake and Mcp-Session-Id, requires Mcp-Method and Mcp-Name headers, replaces server-initiated elicitation and sampling with Multi Round-Trip Requests, deprecates Dynamic Client Registration in favor of Client ID Metadata Documents, and moves Tasks into an extension. Roots, Sampling, and Logging are deprecated with at least a twelve-month window.",
    "url": "https://blog.modelcontextprotocol.io/posts/2026-07-28/",
    "source_title": "The 2026-07-28 Specification",
    "author": "David Soria Parra and Den Delimarsky", "date": "2026-07-28",
    "confidence": "high", "independence": "primary",
    "notes": "Authorization requirements also in the spec page fetched the same day."
  },
  {
    "id": "C40", "cluster": "mcp",
    "claim": "When MCP authorization is implemented, the spec requires OAuth 2.1, protected-resource metadata (RFC 9728), and a Bearer token on every HTTP request. STDIO transports should take credentials from the environment instead of this HTTP flow.",
    "url": "https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization",
    "source_title": "MCP authorization",
    "author": "MCP maintainers", "date": "2026-07-28",
    "confidence": "high", "independence": "primary",
    "notes": ""
  },
  {
    "id": "C41", "cluster": "practice",
    "claim": "Simon Willison's 6 Feb 2025 page quotes Andrej Karpathy naming 'vibe coding': accept all suggestions, do not read the diffs, paste errors back with no comment, and treat it as amusing for throwaway weekend projects. The quoted example prompt is 'decrease the padding on the sidebar by half.'",
    "url": "https://simonwillison.net/2025/Feb/6/andrej-karpathy/",
    "source_title": "A quote from Andrej Karpathy",
    "author": "Andrej Karpathy, quoted by Simon Willison", "date": "2025-02-06",
    "confidence": "high", "independence": "secondary",
    "notes": "Willison is quoting Karpathy's post. The X permalink was not fetched. Ars Technica dates the post to 2 Feb 2025."
  },
  {
    "id": "C42", "cluster": "practice",
    "claim": "Ars Technica quotes Simon Willison distinguishing vibe coding from using an LLM as a typing assistant: if you have reviewed, tested, and understood every line, he does not call it vibe coding. He calls vibe coding your way to a production codebase clearly risky.",
    "url": "https://arstechnica.com/ai/2025/03/is-vibe-coding-with-ai-gnarly-or-reckless-maybe-some-of-both/",
    "source_title": "Will the future of software development run on vibes?",
    "author": "Simon Willison, quoted by Ars Technica", "date": "2025-03",
    "confidence": "medium", "independence": "secondary",
    "notes": "Quote read from the search extract of the article, not a full fetch. Link-checked."
  },
  {
    "id": "C43", "cluster": "repos",
    "claim": "Matt Pocock's README says his skills are small, adaptable, and composable, and that GSD, BMAD, and Spec-Kit take control away by owning the process. Claude Code install in that README is `claude plugin install mattpocock-skills@claude-plugins-official`. Other agents use `npx skills@latest add mattpocock/skills`. He tells you to run /setup-matt-pocock-skills once per repo and to use /grill-me or /grill-with-docs before a change.",
    "url": "https://github.com/mattpocock/skills",
    "source_title": "mattpocock/skills README",
    "author": "Matt Pocock", "date": "README on main, fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "Raw README fetched. Star count not recorded."
  },
  {
    "id": "C44", "cluster": "repos",
    "claim": "Jesse Vincent's Superpowers README calls the skills mandatory workflows, not suggestions. The basic workflow is brainstorming, git worktrees, writing plans, subagent-driven development or executing plans, test-driven development, code review, and finishing the branch. Claude Code install shown is `/plugin install superpowers@claude-plugins-official`. Antigravity install shown is `agy plugin install https://github.com/obra/superpowers`. Muse install shown is `muse plugins install` plus `muse plugins approve superpowers`.",
    "url": "https://github.com/obra/superpowers",
    "source_title": "obra/superpowers README",
    "author": "Jesse Vincent", "date": "README on main, fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "README also names a Grok Build CLI install section. That product's own docs were not fetched."
  },
  {
    "id": "C45", "cluster": "repos",
    "claim": "Hallmark's README, in the repo owned by GitHub user Nutlope (profile name Hassan El Mghari), says it is a design skill for Claude Code, Codex, Cursor, and OpenCode, made by Together AI, with fifty themes. Install shown is `npx skills add nutlope/hallmark -g`. It defines Floor, Reflex, and Finish gates and the verbs `/hallmark redesign` and `/hallmark audit`.",
    "url": "https://github.com/Nutlope/hallmark",
    "source_title": "Nutlope/hallmark README",
    "author": "Hassan El Mghari", "date": "README on main, fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "GitHub profile name checked 2026-11-20 and lists no employer. Together AI is the README's credit. A third-party review describing 20 themes and a .cursor/rules install is stale relative to this README."
  },
  {
    "id": "C46", "cluster": "repos",
    "claim": "Julius Brussee's caveman README says `npx @caveman-ai/cli@latest` installs the tool and needs Node.js 22.13+. It describes six parts: say less, read less, Auto, Blocks, waste fixes, and browse. The Terminal-Bench comparison is the author's, on a measured build with benchmark settings that are not the shipped app. GitHub API on 2026-11-20 reported 121,737 stars, Apache-2.0, and a push at 2026-11-20T07:32:16Z.",
    "url": "https://github.com/JuliusBrussee/caveman",
    "source_title": "JuliusBrussee/caveman README",
    "author": "Julius Brussee", "date": "2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "Benchmark numbers are vendor-measured. The cited arXiv papers were not re-read."
  },
  {
    "id": "C47", "cluster": "repos",
    "claim": "Lauren Tan's pstack README in cursor/plugins says she has worked at Meta, Netflix, and Cursor and is on the React core team. Install in Cursor is `/add-plugin pstack`, then `/setup-pstack`, then `/poteto-mode`. The README lists 22 playbooks. Out of the box, code, prose, and judgment go to Opus 5.5 at xhigh; the default review panel is Fable 5.2, Opus 5.5, and Gemini 4 Neon. Claude Code install is the cursor-plugins marketplace.",
    "url": "https://github.com/cursor/plugins/blob/main/pstack/README.md",
    "source_title": "pstack README",
    "author": "Lauren Tan", "date": "README on main, fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "Employment claims are her own README. Pull request 73, merged 23 May 2026, identifies the plugin as hers. Model defaults can change with /setup-pstack."
  },
  {
    "id": "C48", "cluster": "repos",
    "claim": "The pstack README's published examples include a scroll-drift bug prompt that says to reproduce first, an overnight 'land the stack' prompt, `/how` about cancel-run N+1 queries, and `/interrogate review this pr.` It says /interrogate keeps only findings a run proves, and /arena runs N parallel attempts.",
    "url": "https://github.com/cursor/plugins/blob/main/pstack/README.md",
    "source_title": "pstack README",
    "author": "Lauren Tan", "date": "README on main, fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "These are her documented invocations, not a transcript of a private session."
  },
  {
    "id": "C49", "cluster": "practice",
    "claim": "Anthropic's best-practices table says the last word on a change is branch protection and a person who approves the merge, while Claude's summary of what it did is non-deterministic.",
    "url": "https://code.claude.com/docs/en/best-practices",
    "source_title": "Best practices for Claude Code",
    "author": "Anthropic", "date": "fetched 2026-11-20",
    "confidence": "high", "independence": "primary",
    "notes": "This is the verification principle used on the principles page."
  },
  {
    "id": "C50", "cluster": "claude",
    "claim": "InfoQ's January 2026 article repeats Boris Cherny's parallel-session, plan-mode, CLAUDE.md, slash-command, hook, and Chrome-extension verification account, and quotes the plan-mode sentence about one-shotting a PR after the plan is good.",
    "url": "https://www.infoq.com/news/2026/01/claude-code-creator-workflow/",
    "source_title": "Inside the Development Workflow of Claude Code's Creator",
    "author": "InfoQ", "date": "2026-01",
    "confidence": "medium", "independence": "echo",
    "notes": "Echo of C22. Not an independent origin. Kept so the ledger shows the echo rule."
  },
  {
    "id": "C51", "cluster": "muse",
    "claim": "Reuters on 5 Aug 2026 reported Meta's Muse Code launch, the Muse Spark 1.2 pairing, sub-agents, the action log, and standard-tier prices of $1.25 per million input tokens and $4.25 per million output tokens.",
    "url": "https://www.reuters.com/technology/meta-launches-new-ai-coding-tool-powered-by-muse-spark-12-2026-08-05/",
    "source_title": "Meta launches new AI coding tool powered by Muse Spark 1.2",
    "author": "Reuters", "date": "2026-08-05",
    "confidence": "medium", "independence": "echo",
    "notes": "Echo of Meta's launch post and pricing. Not a second measurement."
  },
  {
    "id": "C52", "cluster": "claude",
    "claim": "TechCrunch on 22 Oct 2026 described Claude Duet as Anthropic's proactive agent for professionals and small businesses, with a cloud virtual machine and approval stops, and reported Anthropic's distinction from personal errands.",
    "url": "https://techcrunch.com/2026/10/22/claude-duet-app-is-anthropics-bet-on-agents/",
    "source_title": "Claude Duet app is Anthropic's bet on agents",
    "author": "TechCrunch", "date": "2026-10-22",
    "confidence": "medium", "independence": "echo",
    "notes": "Echo of C11-C13. Date is one day before the Anthropic article's dateline used here."
  },
]


def main() -> None:
    rows = list(CLAIMS)
    extra = ROOT / "data" / "pass2-claims.json"
    if extra.exists():
        more = json.loads(extra.read_text(encoding="utf-8"))
        have = {row["id"] for row in rows}
        rows.extend(row for row in more if row["id"] not in have)
    data = ROOT / "data"
    data.mkdir(exist_ok=True)
    (data / "sources.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    with (data / "sources.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    js = "window.HUB_CLAIMS = " + json.dumps(rows) + ";\n"
    (ROOT / "js" / "claims.js").write_text(js, encoding="utf-8")
    print(f"wrote {len(rows)} claims")


if __name__ == "__main__":
    main()
