"""
qa_inputs.py — the operator inputs a container QA run accepts, and their checks.

Shared by entrypoint.py (the Cloud Run job) and trigger/main.py (the HTTP
endpoint) so both start paths validate the same way. Inputs travel as
environment variables named QA_<FIELD in upper case>.
"""
from __future__ import annotations

# mode -> (skill folder under skills/qa, skill name, required fields)
MODES = {
    "batch-qa-aecn": ("batch-qa-aecn", "qa-batch-aecn", ["batch_id", "certify_url", "drive_folder"]),
    "batch-qa-charm": ("batch-qa-charm", "qa-batch-charm", ["batch_id", "certify_url", "drive_folder"]),
    "batch-qa-kerry": ("batch-qa-kerry", "qa-batch-kerry", ["batch_id", "certify_url", "drive_folder"]),
    "site-emissions-qa": ("site-emissions-qa", "qa-site-emissions",
                          ["reporting_period", "certify_url", "drive_folder", "site"]),
    # Operator-started replacement for the scheduled Slack sweep: the operator
    # confirms Garrett has finished, the container re-reviews that one batch.
    "re-review": ("garrett-completion-monitor", "qa-garrett-completion-monitor", ["batch_id"]),
}

# Gates each mode runs, one Claude session per gate (entrypoint.py). The gate
# numbers are the skill's own "### GATE n" headings. re-review is short and
# runs as a single session.
GATES = {
    "batch-qa-aecn": [1, 2, 3, 4],
    "batch-qa-charm": [1, 2, 3, 4],
    "batch-qa-kerry": [1, 2, 3, 4],
    "site-emissions-qa": [1, 2, 3],   # Gate 3 includes "After Gate 3" utilities and delivery
    "re-review": [],
}

# Knowledge Base slice each mode reads (knowledge-base/slices/<name>.md, built
# by kb_slices.py). None = read the full Knowledge Base.
KB_SLICE = {
    "batch-qa-aecn": "aecn",
    "batch-qa-charm": "charm",
    "batch-qa-kerry": "kerry",
    "site-emissions-qa": "site-emissions",
    "re-review": None,
}

# Models a run may use. The job default is set in deploy.sh (QA_MODEL); a run can
# override it with the "model" input, e.g. to compare models on the same batch
# in the parity runs before choosing the cheapest one that holds quality.
MODELS = ["claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5"]

FIELDS = [
    "mode",             # one of MODES
    "batch_id",         # e.g. INJ-09-2026-W2 (legacy 2-xxx IDs still accepted)
    "certify_url",      # Certify removal URL(s); comma-separated for multiple scapegoat removals
    "drive_folder",     # batch / RP Site Emissions Drive folder URL
    "reporting_period", # e.g. 2026-09-01 to 2026-09-30
    "site",             # Basco 6 | Vaulted Deep KS
    "cobb_row",         # optional
    "publish_folder",   # optional Drive folder for results; defaults to drive_folder
    "notes",            # optional free text for the agent, e.g. answers to its last questions
    "start_gate",       # optional: re-run from this gate even if later gates were recorded complete
    "model",            # optional: one of MODELS; overrides the job default for this run
    "operator",         # who started the run (filled in by the trigger / CLI)
]


def env_name(field: str) -> str:
    return "QA_" + field.upper()


def validate(inputs: dict) -> list[str]:
    """Return a list of problems; empty means the run can start."""
    problems = []
    mode = inputs.get("mode")
    if mode not in MODES:
        return [f"mode must be one of {sorted(MODES)}, got {mode!r}"]
    for f in MODES[mode][2]:
        if not (inputs.get(f) or "").strip():
            problems.append(f"{mode} needs {f}")
    if inputs.get("model") and inputs["model"] not in MODELS:
        problems.append(f"model must be one of {MODELS}, got {inputs['model']!r}")
    sg = inputs.get("start_gate")
    if sg and (not sg.isdigit() or int(sg) not in GATES[mode]):
        problems.append(f"start_gate must be one of {GATES[mode]} for {mode}")
    unknown = set(inputs) - set(FIELDS)
    if unknown:
        problems.append(f"unknown fields: {sorted(unknown)}")
    return problems
