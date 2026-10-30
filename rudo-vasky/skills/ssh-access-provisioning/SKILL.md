---
name: ssh-access-provisioning
description: Use when provisioning passwordless SSH to a remote host.
metadata:
  hermes:
    tags: [ssh, linux, network]
---

# SSH access provisioning (from `pc-agent` to a remote Linux host)

## When to Use
The user gives an account + one-time password (in chat, or in a file they dropped, usually under `/home/rugent/`) and wants durable key-based SSH access afterwards, then removal of the password material.

## Steps
1. Read only what's needed (account = line 1); `chmod 600` the cred file; never echo the password line.
2. Key: `ssh-keygen -t ed25519 -f ~/.ssh/<alias> -N '' -C 'rudo-vasky@pc-agent' -q`.
3. Copy pubkey using a one-time password WITHOUT sshpass (not installed; global installs are banned here). SSH_ASKPASS works because the terminal tool runs without a tty:
   ```
   printf '#!/bin/sh\nsed -n 2p <credfile>\n' > /tmp/askpass.sh; chmod 700 /tmp/askpass.sh
   SSH_ASKPASS=/tmp/askpass.sh SSH_ASKPASS_REQUIRE=force setsid ssh-copy-id -i <alias>.pub -o StrictHostKeyChecking=accept-new -f <user>@<ip>
   ```
   `setsid` detaches the tty so ssh takes the askpass path; `-f` copies the key without running a remote command; exit 0 = installed.
4. Verify key-only login with `-o BatchMode=yes` to EVERY address the access should cover (LAN IP and tailnet IP separately).
5. Each extra IP needs its own known_hosts entry: `ssh-keyscan -t ed25519 <ip> >> ~/.ssh/known_hosts` — "Host key verification failed" on a second IP of a working host just means missing entry, not a wrong host. To rule out MITM, diff the ed25519 key material between the two IPs — they must be identical.
6. Register an alias in `~/.ssh/config`: shared block `Host <a> <a>-lan <a>-tn` with `User`, `IdentityFile`, `IdentitiesOnly yes`, then per-IP `HostName` blocks so LAN and tailnet each have an explicit target.
7. Delete the cred file and the askpass script, and verify they are gone before reporting success.

## Pitfalls
- Reinstalled/renumbered box → REMOTE HOST IDENTIFICATION HAS CHANGED: `ssh-keygen -R <ip>` then reconnect with `StrictHostKeyChecking=accept-new`; mention it to the user, don't silently ignore.
- `BatchMode` Permission denied (publickey,password) before key install is expected — it means auth, not network; that's why the askpass copy step comes first.
