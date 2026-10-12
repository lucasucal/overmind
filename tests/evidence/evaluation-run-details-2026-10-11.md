# Evaluation run details

Decision evaluations now show the same run-details card structure as response
evaluations: participant model chips, baseline, pinned dataset/version links,
row counts, optional calibration dataset and capability, timestamps and status.
The existing prepare, launch and pause controls sit in the card footer. Completion
time uses the completed scoring receipt's observation; otherwise the card labels
the last update. Native credit usage has no ledger total on this response and
remains unmeasured. The Optimise action is removed from response evaluation details.

Failure cases recorded in the browser journey before implementation: no details
on probability runs; displaying a later dataset version's row count; missing
calibration data; inventing a separate judge; broken pinned dataset links; and
retaining the Optimise action on completed response runs.

## Reproduction

Environment: local compose PostgreSQL on port 5432 and Redis on port 6379, uv and
Bun dependencies installed, and Playwright Chromium available. The browser journey
uses the disposable test database and Redis DB 15; run database tests sequentially.

- `make test-journeys test_args='-k test_evaluations_share_runs_navigation_and_probability_metrics'`
  — 1 passed, 68 deselected. Fixture: completed response run and probability
  comparison, a pinned 10-row final cell with a newer 999-row cell, and a separate
  3-row calibration cell. It checks model/baseline details, exact links, counts,
  timestamps, no judge field and no Optimise action. First attempt used a substring
  check that also matched sidebar Optimiser; the corrected exact-action assertion
  passed. Log: `/private/tmp/evaluation-details-journey-retest.log`. Receipts:
  `tests/journeys/.runs/20261011T172252Z/`.
- `uv run pytest -q tests/test_native_evaluation_plan.py::test_native_plan_api_is_idempotent_and_project_scoped`
  — 1 passed. Log: `/private/tmp/evaluation-details-api.log`.
- From `frontend/`: `bun run typecheck`, `bun run lint`, `bun run check:all`
  — passed. Logs: `/private/tmp/evaluation-details-{typecheck,lint,design}.log`.
- `make generate_api_client` regenerated the typed `final_suite` and
  `calibration_suite` metadata. No generated file was edited by hand.

Manual browser check: local Jev validation project
`a279d834-899c-4ac6-888a-157f0c7d9cf8`, six-model Titanic comparison
`9e1b9caa-858b-48ef-8af6-9e701bd99132`. The card shows all six participants,
the baseline, the named 625-row dataset pinned at version 2.0, recorded creation
and completion dates, and completed status with full-width dividers. Screenshot:
`/private/tmp/evaluation-run-details.jpg`.

MCP impact: none. Native comparison lifecycle, configuration and scoring receipts
are unchanged. The additive REST display metadata reads the same pinned cells.
No evaluation, training or provider request was launched for verification.
