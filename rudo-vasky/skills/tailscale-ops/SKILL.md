---
name: tailscale-ops
description: Use when configuring Tailscale routes or status here.
version: 1
author: rudo-vasky
metadata:
  hermes:
    tags: [tailscale, network, vpn]
---

# Tailscale ops (host `pc-agent`, tailnet IP 100.103.72.54, LAN 192.168.16.0/24)

## When to Use
The user asks to check, start/stop, or reconfigure Tailscale on this host — expose a LAN machine to the tailnet, find the tailnet IP, or locate the authentication keys.

## Check state
- `tailscale status` — peers and connection state; `tailscale status --peers=false` for self.
- If it says "failed to connect to local tailscaled", the service is down: `sudo systemctl start tailscaled` (stopping it is a system-service action — expect approval prompt).

## Subnet router (expose LAN host(s) to the tailnet)
1. `sudo tailscale set --advertise-routes=<CIDR>` — plain `tailscale set` fails with "Access denied: checkprefs access denied"; always use sudo (or once: `sudo tailscale set --operator=$USER`).
2. Verify with `tailscale debug prefs | grep -A2 AdvertiseRoutes` — the `Self` JSON from `tailscale status --json` does NOT reliably show AdvertisedRoutes; don't conclude failure from it.
3. Remind the user to approve the route in the admin console (login.tailscale.com/admin/machines → node → subnet routes); an unapproved route never activates.
4. Reachability from the tailnet uses the LAN IP itself (e.g. ssh 192.168.16.243), not a 100.x address.

## Tear down (user prefers no standing subnet router)
- Clear routes with `sudo tailscale set --advertise-routes=` (empty value), then `sudo systemctl stop tailscaled`. The user typically wants the tunnel up only transiently while a remote box gets set up, then off again.

## Standing SSH access to LAN hosts
Known hosts reachable from pc-agent:
- **gx10** (`gx10-db82`): user `rudgx`, LAN `192.168.16.243`, tailnet `100.89.31.20`; key `~/.ssh/pc-gx10`, aliases in `~/.ssh/config` — `ssh gx10` (LAN), `ssh gx10-tn` (tailnet). Key-based, passwordless.

To grant standing key access to a new host when only a password is available (`sshpass` is not installed and global installs are banned):
1. Have the user put credentials in a file (line 1 account, line 2 password) and tell you the path; read only line 1 yourself so the password never enters chat.
2. `ssh-keygen -t ed25519 -f ~/.ssh/<host> -N ''`.
3. Non-interactive copy: write an askpass helper that `sed -n 2p` the password file, then `SSH_ASKPASS=<helper> SSH_ASKPASS_REQUIRE=force setsid ssh-copy-id -i <key>.pub -o StrictHostKeyChecking=accept-new -f <user>@<ip>` — `setsid` detaches the tty so ssh uses the askpass helper instead of prompting.
4. Add a `~/.ssh/config` block with per-IP aliases (LAN + tailnet), then `shred`/`rm` the credentials file and the helper.

## Pitfalls
- Advertise a single `/32` per host, not the whole `/24`, unless asked — the user considers full-subnet exposure too risky and will ask to narrow it.
- `tailscale set` has no `--reset` flag in the installed version; it only changes flags you name.
- Machine/authentication state lives in `/var/lib/tailscale/tailscaled.state` (contains the Machine Key). Stopping or restarting `tailscaled` does NOT log the node out — on start it rejoins the tailnet silently, so no browser auth link appears. To force browser re-auth: `sudo tailscale logout` then `sudo tailscale up` (the up command prints the login URL and waits; run it in the background and forward the URL to the user).
- SSH to a LAN box failing with known-key mismatch: `ssh-keygen -R <ip>` then reconnect with `StrictHostKeyChecking=accept-new` (reinstalled box); auth still needs the right account — BatchMode as local user fails with Permission denied if no key is authorized.
- A host reachable via both LAN and tailnet IP is a NEW known host on the second IP: `ssh-keyscan` it and diff its ed25519 key against the LAN IP's — a mismatch while you expect the same box means wrong host, not a reimage.
- Other tailscale features for this user: exit node (overkill for one host), `tailscale set --ssh` (tailnet-policy SSH), Funnel/Serve (web only, not for SSH).
