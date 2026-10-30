# Hermes Profile Templates

Sanitized templates for Hermes Agent profiles — behavioral configuration (SOUL.md, MEMORY.md), profile structure, and custom skills. **No credentials, tokens, or runtime state included.**

## Structure

```
hermes-profile-template/
├── rudo-vasky/           # RudoVasky — Slovak Discord bot (Cheaterina community)
│   ├── SOUL.md           # Personality & behavior rules
│   ├── MEMORY.md         # Behavioral memory (sanitized)
│   ├── profile.yaml      # Profile structure
│   ├── config.yaml.template  # Config with placeholders
│   ├── .env.example      # Environment variables template
│   ├── skills/           # Custom skills (profile-specific)
│   │   ├── discord-bot-ops/
│   │   ├── oberon-licence-activation/
│   │   ├── ssh-access-provisioning/
│   │   └── tailscale-ops/
│   ├── scripts/          # Custom scripts
│   └── assets/           # Images, static files
│
└── hadajner/             # Hadajner — Slovak Discord chatbot (conspiracy/humor)
    ├── SOUL.md           # Personality & behavior rules
    ├── MEMORY.md         # Behavioral memory (sanitized)
    ├── profile.yaml      # Profile structure
    ├── config.yaml.template  # Config with placeholders
    ├── .env.example      # Environment variables template
    ├── skills/           # Custom skills
    │   └── hadajner-baza/      # Knowledge base skill
    ├── scripts/          # Custom scripts
    └── assets/           # Images, static files
```

## What's Included

| File | Purpose |
|------|---------|
| `SOUL.md` | Core personality, tone, language rules, tool usage |
| `MEMORY.md` | Behavioral patterns, preferences, interaction rules (sanitized) |
| `profile.yaml` | Profile metadata (name, model, provider) |
| `config.yaml.template` | Runtime config with `YOUR_*` placeholders |
| `.env.example` | Environment variables template |
| `skills/` | **Custom skills only** (not bundled Hermes skills) |
| `scripts/` | Profile-specific utility scripts |
| `assets/` | Images, static files |

## What's EXCLUDED (Security)

| Excluded | Reason |
|----------|--------|
| `.env` | Contains real tokens, API keys |
| `config.yaml` | Contains real credentials |
| `state.db*` | Conversation history, memories, sessions |
| `projects.db*` | Project data |
| `sessions/` | Full chat history |
| `memories/` | Long-term memories (may contain PII) |
| `cache/` | Cached API responses, embeddings |
| `logs/` | May contain tokens in debug output |
| `runtime/` | Runtime state |
| `*.lock` | Lock files |
| `.skills_prompt_snapshot.json` | Internal state |
| `provider_models_cache.json` | Model metadata |

## Usage

### 1. Create New Profile from Template

```bash
# Copy template to new profile directory
cp -r hermes-profile-template/rudo-vasky ~/.hermes/profiles/my-rudovasky

# Fill in credentials
cd ~/.hermes/profiles/my-rudovasky
cp config.yaml.template config.yaml
cp .env.example .env

# Edit with your values
vim config.yaml
vim .env
```

### 2. Required Credentials

| Variable | Source |
|----------|--------|
| `DISCORD_BOT_TOKEN` | Discord Developer Portal → Bot → Token |
| `DISCORD_HOME_CHANNEL` | Right-click channel → Copy ID (Developer Mode) |
| `FIRECRAWL_API_KEY` | firecrawl.dev dashboard |
| `HERMES_CUSTOM_127_0_0_1_4000_API_KEY` | LiteLLM proxy key |
| `SEARXNG_URL` | Your SearXNG instance |

### 3. Install Custom Skills

The `skills/` directory contains profile-specific skills. Bundled Hermes skills (autonomous-ai-agents, github, etc.) are installed separately via Hermes skill system.

```bash
# Skills are ready to use — Hermes loads them from profile/skills/
# No additional installation needed for custom skills
```

## Profile Differences

| Aspect | rudo-vasky | hadajner |
|--------|------------|----------|
| **Persona** | Fun Discord bot, "HEIL VASKY!", "Takže tak!" | Conspiracy/humor chatbot, "Šéfino" |
| **Language** | Slovak, proper grammar, short sentences | Slovak, mixes conspiracy knowledge base |
| **Knowledge Base** | General + user preferences | `hadajner-baza` skill (conspiracy theories, riddles) |
| **Discord** | Replies to @mention, "HEIL VASKY!" opener for specific user | Replies to @mention, "Šéfino" for specific user |
| **Tools** | web_search, vision, TTS, memory | skill_view (hadajner-baza), memory, web_search |
| **Custom Skills** | discord-bot-ops, oberon-licence-activation, ssh-access-provisioning, tailscale-ops | hadajner-baza |

## Security Checklist

Before using a profile from this template:

- [ ] All `YOUR_*` placeholders replaced in `config.yaml` and `.env`
- [ ] No real tokens in any committed file
- [ ] `config.yaml` and `.env` are in `.gitignore`
- [ ] No `state.db*`, `projects.db*`, `sessions/`, `memories/` committed
- [ ] Custom skills reviewed for hardcoded secrets
- [ ] Discord bot token has minimal required scopes

## License

MIT — Use freely for your own Hermes profiles.
