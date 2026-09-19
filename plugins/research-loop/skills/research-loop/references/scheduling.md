# Private scheduling

Read `get_my_planning_context` before authorized schedule changes. It combines current work across the human owner's active projects with cached busy intervals from their primary Google calendar, only after opt-in. The read itself makes no Google request and does not replay project history.

1. Check `complete`, timezone, accepted versus tentative work, deadlines and missing estimates. Parent goals organize child tasks; do not count their hours again. Finished individual assignments are not remaining work even if the shared task stays open.
2. Check `externalCalendar.status`, `checkedAt` and window boundaries. Compare actual UTC instants. Disabled, pending, failed, stale or out-of-window data is unknown, never free time. Empty busy intervals do not establish working hours; other calendars are not covered.
3. Ask about unresolved availability, respect fixed deadlines and reserve an agreed buffer. Suggest a short schedule with priority/scope/date tradeoffs; do not invent consent or move external deadlines.
4. Write only the authorized change with `planning_context_token` and `planning_rationale`. Refresh after a scheduling write or a stale token. A token verifies a snapshot, not feasibility or a global reservation.

Never copy private busy times or other-project names, IDs or schedules into shared pages. Give only a generic capacity constraint. New Google consent is a human action in personal settings. This integration imports availability and exports Research Loop schedules; it does not turn Google event edits into shared research edits or keep a closed AI client running.
