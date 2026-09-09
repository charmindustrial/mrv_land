# Garrett — MRV request sender setup (covers July 1 while Max is out)

This stands up a tiny sender on your Mac that emails the three June reporting requests from g_mrv@ on July 1, so they go out while Max is away (7/1–7/8). It needs **no Claude Code** — just Python (built into macOS dev tools) and two credential files. Reminders and all the data processing resume on Max's Mac when he's back on the 8th; this is requests-only.

**Whole thing takes ~5 minutes. Steps 1–2 are the only manual bits.**

---

## What you'll receive from Max

Two small files (via 1Password or a restricted Drive share — not email/Slack):
- `gcp-oauth.keys.json`
- `credentials.json`

These are the mailbox login. Keep them only as long as needed; teardown (bottom) deletes them.

---

## 1. Put the files in place

```sh
# the sender script (also in the MRV workspace repo if you have it)
mkdir -p ~/mrv-requester
# → save standalone_requester.py into ~/mrv-requester/

# the credential files Max sent you
mkdir -p ~/.gmail-mcp
# → save gcp-oauth.keys.json and credentials.json into ~/.gmail-mcp/
```

## 2. Confirm Python is present

```sh
python3 --version
```
If that prints a version, you're set. If it says "command not found," run `xcode-select --install`, click through the installer, then re-check.

## 3. Test it (sends nothing)

```sh
DRY_RUN=1 python3 ~/mrv-requester/standalone_requester.py
```
- Before July 1, you'll see: *"before go-live … live sends begin July 1."* That's correct.
- It should reach the mailbox without errors. If you see a token error, the credential files aren't in `~/.gmail-mcp/` or didn't copy cleanly.

## 4. Schedule it (runs a few times a day, and catches up on wake)

Paste this whole block once:

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
    <string>$HOME/mrv-requester/standalone_requester.py</string>
  </array>
  <key>StartCalendarInterval</key>
  <array>
    <dict><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
    <dict><key>Hour</key><integer>12</integer><key>Minute</key><integer>0</integer></dict>
    <dict><key>Hour</key><integer>16</integer><key>Minute</key><integer>0</integer></dict>
  </array>
  <key>StandardOutPath</key><string>$HOME/mrv-requester/run.log</string>
  <key>StandardErrorPath</key><string>$HOME/mrv-requester/run.log</string>
</dict>
</plist>
PLIST
launchctl load ~/Library/LaunchAgents/com.charm.mrv-requester.plist
echo "scheduled."
```

macOS may pop up "python wants to access files" the first time — click **Allow** (it's the script reading its own credential files).

## 5. Confirm on July 1

After the morning of the 1st, check it sent:
```sh
cat ~/mrv-requester/run.log
```
You want to see three "sent ->" lines (Community / Wellhead / Oxidizer). You can also glance at g_mrv@'s Sent folder. If your Mac was asleep at 8am, it fires when the Mac next wakes — the requests still go out that day.

It's safe if it runs again — it checks the mailbox first and won't re-send.

---

## Teardown (when Max is back, ~July 8)

```sh
launchctl unload ~/Library/LaunchAgents/com.charm.mrv-requester.plist
rm ~/Library/LaunchAgents/com.charm.mrv-requester.plist
rm ~/.gmail-mcp/gcp-oauth.keys.json ~/.gmail-mcp/credentials.json
```
That removes the schedule and deletes the mailbox credential from your Mac. Max's Mac takes back over as primary.

Questions: ping Max (or he'll have briefed you).
