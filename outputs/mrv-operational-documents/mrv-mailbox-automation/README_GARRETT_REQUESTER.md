# Garrett — MRV July 1 request sender (one-week stopgap)

**Why:** Max is out July 1–8 with his Mac off, and the monthly MRV request must go out on July 1. This is a tiny self-contained sender that runs on **your** Mac just to send the three June-2026 requests on July 1. Reminders and all data processing resume automatically on Max's Mac when he's back on the 8th — you don't need to do anything with those.

**What it needs:** only macOS (Python and curl are already built in). **No Claude Code, no workspace clone.** Just two credential files + one script + a schedule.

**It's safe:** it checks the shared mailbox before sending, so it can't double-send, and it won't clash when Max's Mac comes back online. It can only send (it can't delete or read anything beyond checking what's already been sent). It will not send anything before July 1.

---

## Step 1 — Get the credential (from Max, securely)

Max will **AirDrop** you two files (do not send these over Slack/email — they're the mailbox login):
- `gcp-oauth.keys.json`
- `credentials.json`

Put both in a folder named `.gmail-mcp` in your home folder. In Terminal:

```sh
mkdir -p ~/.gmail-mcp
# then move the two AirDropped files into it, e.g.:
mv ~/Downloads/gcp-oauth.keys.json ~/Downloads/credentials.json ~/.gmail-mcp/
```

## Step 2 — Get the sender script

Put `standalone_requester.py` (from this same folder in the MRV workspace, or Max sends it) into `~/.gmail-mcp/`:

```sh
mv ~/Downloads/standalone_requester.py ~/.gmail-mcp/
```

## Step 3 — Verify it works (sends nothing)

```sh
DRY_RUN=1 python3 ~/.gmail-mcp/standalone_requester.py
```

Expected before July 1: a line saying it's before go-live and that on/after July 1 it will send the previous-month request. Expected on/after July 1: three "WOULD SEND" lines for Alison, Casey, Evan. If you see a token error, the credential files aren't in place — recheck Step 1.

## Step 4 — Install the schedule

This makes your Mac run the sender a few times a day (and catch a missed run when it wakes). Paste this whole block into Terminal:

```sh
cat > ~/Library/LaunchAgents/com.charm.mrv-requester.plist <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.charm.mrv-requester</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>$HOME/.gmail-mcp/standalone_requester.py</string>
  </array>
  <key>StartCalendarInterval</key>
  <array>
    <dict><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
    <dict><key>Hour</key><integer>12</integer><key>Minute</key><integer>0</integer></dict>
    <dict><key>Hour</key><integer>16</integer><key>Minute</key><integer>0</integer></dict>
  </array>
  <key>RunAtLoad</key><true/>
  <key>StandardOutPath</key><string>$HOME/.gmail-mcp/requester.log</string>
  <key>StandardErrorPath</key><string>$HOME/.gmail-mcp/requester.err.log</string>
</dict>
</plist>
PLIST
launchctl bootout gui/$(id -u)/com.charm.mrv-requester 2>/dev/null
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.charm.mrv-requester.plist
echo "installed."
```

macOS may pop up "python wants to access files" — click **Allow** (it needs to read the credential file). It runs immediately on install; before July 1 that's a harmless no-op.

## Step 5 — Confirm on July 1

After July 1, check the log:

```sh
cat ~/.gmail-mcp/requester.log
```

You want to see three "sent ->" lines. You can also look in g_mrv@'s Sent folder for the three `MRV reporting request — June 2026` emails. Once they're sent, every later run just says "already sent, skipping" — that's correct.

## Teardown (when Max is back, optional)

It's harmless to leave running (it won't re-send), but to remove it cleanly:

```sh
launchctl bootout gui/$(id -u)/com.charm.mrv-requester
rm ~/Library/LaunchAgents/com.charm.mrv-requester.plist
rm -rf ~/.gmail-mcp   # removes the credential files from your Mac
```

Questions: ping Max (or Claude in the MRV workspace).
