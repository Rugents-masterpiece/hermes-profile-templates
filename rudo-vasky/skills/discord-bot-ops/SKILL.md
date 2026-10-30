---
name: discord-bot-ops
description: Use for joining Discord servers and verifying membership.
metadata:
  hermes:
    tags: [discord, bot]
---

# Discord bot ops (RudoVasky gateway bot)

## Joining a new server
A bot cannot join itself — a human with server admin must authorize it. Send the ready-made link (app id below):
`https://discord.com/oauth2/authorize?client_id=1493587794189353010&scope=bot&permissions=1117184`
(permissions int = View Channels + Send Messages + Read Message History + Add Reactions — matches what the persona needs.)

- The app id is derived from the bot token, no console needed: first dot-separated segment of `DISCORD_BOT_TOKEN` (in the profile `.env`) is the app id base64url-encoded — `echo "$tok" | cut -d. -f1 | base64 -d`. Never print the token itself.

## Verifying membership
`curl -s -H "Authorization: Bot $tok" https://discord.com/api/v10/users/@me/guilds` → live list of `{id, name}`. Use this, NOT `channel_directory.json` in the profile — that file is a stale gateway cache and misses newly added servers.

## Behavior notes for new servers
- Profile config has `require_mention: true` and `ignored_channels: '*'`: on a fresh server the bot only answers mentions/DMs until the gateway config is adjusted — warn the user once when first joining a new server.
