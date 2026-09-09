#!/usr/bin/env python3
"""
MRV monthly-request standalone sender (absence stopgap).

Purpose: send the three monthly reporting requests from g_mrv@charmindustrial.com
on/after the 1st, with no dependency on Claude Code or the workspace. Built to run
on a second machine (Garrett's Mac) while the primary host is off.

Safe to run repeatedly and alongside the primary host: it checks the shared mailbox
(g_mrv@'s Sent items) before sending, so a request already sent — by this script or
by the full system on the primary Mac — is never re-sent.

Scope: REQUESTS ONLY. Reminders and all intake/processing resume on the primary host.

Setup: needs ~/.gmail-mcp/gcp-oauth.keys.json and ~/.gmail-mcp/credentials.json
(copied from the primary Mac). Uses curl for HTTPS (system certs; avoids the Python
SSL-cert issue on some macOS Python builds).

Run:   python3 standalone_requester.py            # live
       DRY_RUN=1 python3 standalone_requester.py  # show what it would do, send nothing
"""
import json, os, subprocess, base64, urllib.parse, datetime, sys

GMAIL_DIR = os.path.expanduser("~/.gmail-mcp")
KEYS = os.path.join(GMAIL_DIR, "gcp-oauth.keys.json")
CREDS = os.path.join(GMAIL_DIR, "credentials.json")
DRY = os.environ.get("DRY_RUN") == "1"
SENDER = "MRV Shared Mailbox <g_mrv@charmindustrial.com>"

REPORTERS = [
    {"to": "alison@charmindustrial.com", "tag": "[Community]",
     "body": ("Hi Alison,\n\nIt's time for the {period} MRV reporting. Please reply to this email "
              "with the Community Engagement reporting for the period:\n\n"
              "- Updated Events List, and\n- Updated Grievance Record\n\n"
              "(one file or two — both are needed).\n\n"
              "Keeping the [Community] tag in the subject helps it get filed automatically. Thanks!\n\n— MRV Bot")},
    {"to": "casey.korejwo@charmindustrial.com", "tag": "[Wellhead]",
     "body": ("Hi Casey,\n\nIt's time for the {period} MRV reporting. Please reply to this email with the "
              "wellhead injection data for the period (the raw SCADA export is fine — we process it on our end).\n\n"
              "Keeping the [Wellhead] tag in the subject helps it get routed automatically. Thanks!\n\n— MRV Bot")},
    {"to": "evan.Weisenberger@charmindustrial.com", "tag": "[Oxidizer]",
     "body": ("Hi Evan,\n\nIt's time for the {period} MRV reporting. Please reply to this email with the "
              "oxidizer catalyst temperature data for the period (the raw export is fine — we process it on our end).\n\n"
              "Keeping the [Oxidizer] tag in the subject helps it get routed automatically. Thanks!\n\n— MRV Bot")},
]


def curl(args):
    out = subprocess.run(["curl", "-s"] + args, capture_output=True, text=True)
    return out.stdout


def access_token():
    keys = json.load(open(KEYS))["installed"]
    creds = json.load(open(CREDS))
    resp = curl([
        "https://oauth2.googleapis.com/token",
        "-d", "client_id=" + keys["client_id"],
        "-d", "client_secret=" + keys["client_secret"],
        "-d", "refresh_token=" + creds["refresh_token"],
        "-d", "grant_type=refresh_token",
    ])
    tok = json.loads(resp).get("access_token")
    if not tok:
        sys.exit("ERROR: could not refresh access token: " + resp)
    return tok


def already_sent(tok, subject):
    q = urllib.parse.quote('in:sent subject:"%s"' % subject)
    url = "https://gmail.googleapis.com/gmail/v1/users/me/messages?q=" + q
    resp = curl(["-H", "Authorization: Bearer " + tok, url])
    return bool(json.loads(resp).get("messages"))


def send(tok, to, subject, body):
    mime = ("From: %s\r\nTo: %s\r\nSubject: %s\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n%s"
            % (SENDER, to, subject, body))
    raw = base64.urlsafe_b64encode(mime.encode("utf-8")).decode("ascii")
    payload = json.dumps({"raw": raw})
    url = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"
    resp = curl(["-H", "Authorization: Bearer " + tok, "-H", "Content-Type: application/json",
                 "-X", "POST", "-d", payload, url])
    if '"id"' not in resp:
        print("  !! send FAILED:", resp)
        return False
    return True


def period_label(today):
    # Reporting period = the just-completed calendar month.
    first_of_this_month = today.replace(day=1)
    last_month_end = first_of_this_month - datetime.timedelta(days=1)
    return last_month_end.strftime("%B %Y")


GO_LIVE = datetime.date(2026, 7, 1)  # first request ever sent: June 2026 reporting, on/after this date


def main():
    today = datetime.date.today()
    period = period_label(today)
    print("MRV standalone requester — %s — period: %s%s"
          % (today.isoformat(), period, "  [DRY RUN]" if DRY else ""))

    # Go-live guard: never send before July 1, 2026 (prevents a stale pre-go-live month being requested).
    if today < GO_LIVE:
        print("  before go-live (%s) — nothing to send. (On/after July 1 this sends the %s request.)"
              % (GO_LIVE.isoformat(), "previous-month"))
        if not DRY:
            return
        print("  [DRY RUN] continuing to show mechanics only; live sends begin July 1.")

    tok = access_token()
    for r in REPORTERS:
        subject = "%s MRV reporting request — %s" % (r["tag"], period)
        if already_sent(tok, subject):
            print("  already sent, skipping:", subject)
            continue
        body = r["body"].format(period=period)
        if DRY:
            print("  WOULD SEND ->", r["to"], "|", subject)
            continue
        ok = send(tok, r["to"], subject, body)
        print(("  sent -> " if ok else "  FAILED -> ") + r["to"] + " | " + subject)


if __name__ == "__main__":
    main()
