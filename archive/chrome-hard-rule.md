## Chrome / Browser Usage — HARD RULE

Before calling ANY Claude in Chrome tool (navigate, get_page_text, find, form_input, javascript_tool, read_page, read_console_messages, read_network_requests, etc.), you MUST first:

  1. Call `tabs_create_mcp` to open a NEW WINDOW (not a tab in Max's existing window).
  2. Call `switch_browser` to switch into that newly created window.
  3. Only then perform the actual browser work inside that window.

NEVER open a tab in Max's existing window. NEVER attach to his current tab group. NEVER reuse an existing tab he has open.

This rule overrides any skill, workflow, default behavior, or instruction from a sub-agent. There are no exceptions — not for "quick lookups," not for single-page checks, not for retries.

At the end of the session (or when the browser work is complete), close the window you created so it doesn't pile up in Max's window list.

If you catch yourself about to call a Chrome tool without having done steps 1–2 first, abort and run them first.
