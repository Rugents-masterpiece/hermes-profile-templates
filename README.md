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


## 🤝 Contributing

Contributions are welcome! Whether it's bug fixes, new features, documentation improvements, or testing — every contribution helps.

### Ways to Contribute

| Type | Description |
|------|-------------|
| 🐛 **Bug Reports** | Found an issue? Open a GitHub Issue with steps to reproduce, expected vs actual behavior, and environment details |
| ✨ **Feature Requests** | Have an idea? Open a GitHub Issue with the "enhancement" label describing the use case |
| 📝 **Documentation** | Fix typos, clarify setup steps, add examples — PRs to `README.md` or `/docs` are always appreciated |
| 🔧 **Code** | Bug fixes, new features, refactoring, tests |
| 🧪 **Testing** | Test on different hardware/OS, report compatibility |
| 💡 **Ideas & Feedback** | Discussions, RFCs, architecture suggestions |

### Quick Start for Contributors

```bash
# 1. Fork the repository
# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/REPO-NAME.git
cd REPO-NAME

# 3. Create a feature branch
git checkout -b feature/your-feature-name

# 4. Make changes, test locally
# (see README for local development setup)

# 5. Commit with conventional commits
git commit -m "feat: add amazing feature"

# 6. Push and open a Pull Request
git push origin feature/your-feature-name
```

### Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat:     new feature
fix:      bug fix
docs:     documentation only
style:    formatting, no code change
refactor: code restructuring
test:     adding tests
chore:    maintenance, deps, build
```

Examples:
- `feat: add voice selection UI for TTS`
- `fix: handle GPU OOM in model offloading`
- `docs: clarify Docker setup for ARM64`

### Pull Request Guidelines

- ✅ **One feature/fix per PR** — keeps reviews focused
- ✅ **Tests pass** — run local tests before pushing
- ✅ **Update docs** — if behavior changes, update README/comments
- ✅ **No credentials** — never commit `.env`, keys, tokens
- ✅ **Small, focused commits** — easier to review

### Development Setup

See the **Installation** section above for local setup. Most projects use:

```bash
# Python projects
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# or pip install -e ".[dev]" for dev dependencies

# .NET projects
dotnet restore
dotnet build

# Docker projects
docker compose up -d --build
```

### Code Style

| Language | Formatter | Linter |
|----------|-----------|--------|
| Python | `black` | `ruff` |
| C# | `dotnet format` | Built-in |
| JavaScript/TypeScript | `prettier` | `eslint` |
| Blazor | `dotnet format` | Built-in |

Run formatters before committing:
```bash
# Python
black . && ruff check .

# .NET
dotnet format

# JS/TS (if applicable)
prettier --write .
```

### Reporting Security Issues

**Do not open public issues for security vulnerabilities.** Email directly or use GitHub's private vulnerability reporting.

### Community

- 💬 **Discussions**: Use GitHub Discussions for questions, ideas, RFCs
- 🐛 **Issues**: Bug reports, feature requests
- 📧 **Contact**: Open an issue for maintainer contact

### Recognition

Contributors are recognized in:
- GitHub Contributors graph
- Release notes (for significant contributions)
- `AUTHORS.md` or `CONTRIBUTORS.md` (if maintained)

---

**Thank you for contributing!** 🎉

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

MIT License allows:
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ❌ No liability
- ❌ No warranty

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! It helps with visibility and motivation.

## License

MIT — Use freely for your own Hermes profiles.
