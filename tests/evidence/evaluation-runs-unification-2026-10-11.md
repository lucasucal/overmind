# Evaluation Runs consolidation

Failure cases identified before implementation: native results become unreachable
when their tab is removed; two independently paginated lists omit or duplicate
runs; native statuses disappear under filters; tenant or API-key scope broadens;
native records receive generative delete actions; training-linked paired results
lose their original metrics; creation loses calibration or baseline selection.

The API regression covers server-side combined pagination, filters, facets and
tenant scope. Browser verification covers navigation, creation and retained results.

## Reproduction

Environment: local compose PostgreSQL on port 5432, Redis on port 6379, Python
dependencies installed with uv and frontend dependencies installed with Bun. The
journey uses its disposable database, Redis DB 15 and a built Console with
Playwright Chromium. Run database-backed commands sequentially.

Commands and observed results:

- `uv run pytest -q tests/test_evaluation_activity.py tests/test_eval_api.py` — 128 passed.
- From `frontend/`: `bun run test src/components/evaluations/runs-table.test.tsx src/components/evaluations/runs-table.row-click.test.tsx src/components/evaluations/create-run-dialog.test.tsx src/components/model-workflows/workflows.test.tsx` — 17 passed.
- `make test-journeys test_args='-k test_evaluations_share_runs_navigation_and_probability_metrics'` — 1 passed, 68 deselected.
- From `frontend/`: `bun run typecheck`, `bun run lint`, `bun run check:all` — passed.
- Scoped `uv run pre-commit run --files ...` covering the new activity service,
  serializers, generated client, routes, forms, metrics, tests and design document — passed.

Fixtures: a generated-response run and a completed probability comparison share
one project and dataset. A second project's plan tests isolation. The probability
fixture has cross entropy 1.8, seven scored of ten expected observations, three
distinct missing/invalid/incompatible observations, and a recorded paired delta.
The journey opens the comparison from Runs, checks numeric scores above one are
retained, follows the old Decisions URL into Runs, and opens probability setup
through New evaluation. It does not dispatch paid predictions or training.

The first API attempt exposed a duplicate fixture slug; after correcting it, the
test reproduced the missing activity endpoint. The first browser journey reached
the correct form but failed an exact text locator on a label containing a selector.
The corrected text locator passed. An attempted parallel API/journey retest collided
on their shared disposable database; both commands subsequently passed sequentially.

Journey receipts and screenshot:
`tests/journeys/.runs/20261011T073126Z/`. Final API log:
`/private/tmp/evaluation-activity-regression-serial.log`; browser log:
`/private/tmp/evaluation-runs-journey-final.log`.

Manual local verification used the existing Jev validation project
`a279d834-899c-4ac6-888a-157f0c7d9cf8`: both Titanic probability benchmarks appear
beside the saved generated-response evaluations. The before/after comparison
`aeecf56c-6407-4989-bc1f-fd4bc2e6f79c` displays raw and calibrated bars; calibrated
Brier hover reports the stored trained-model value 0.3097. Dataset chips link the
frozen suite cell. Screenshot: `/private/tmp/evaluation-probability-metrics.jpg`.

MCP impact: no changed tool or resource contract. Existing native comparison,
calibration, resume and report services remain authoritative. The additive REST
activity read combines their receipts with generated-response runs for Console
pagination. No provider worker or production deployment is involved.

## Comparison and typography cleanup

Additional failure cases captured before implementation: duplicating the baseline
for every candidate, dropping distinct soft-target metrics because their displayed
values happen to match, retaining removed diagnostic controls, and applying
Mondwest to cards and dialogs instead of only main page titles.

The comparison now has one table with one row per model per benchmark. Hard-label
results omit mode agreement and top-choice reference mass only when their scored
denominators establish that they repeat accuracy. Mixed-target fixtures retain
those metrics. Score denominators, uncertainty and paired differences remain
available on hover; the requested download, diagnostic and performance controls
are absent. Their backend services and records are unchanged.

Verification after cleanup:

- From `frontend/`: `bun run test src/components/model-workflows/workflows.test.tsx`
  — 4 passed. Log: `/private/tmp/evaluation-cleanup-tests.log`.
- `make test-journeys test_args='-k test_evaluations_share_runs_navigation_and_probability_metrics'`
  — 1 passed, 68 deselected. The browser verifies the single table, removed
  sections, main title font and dialog title font. Log:
  `/private/tmp/evaluation-cleanup-journey.log`; receipts:
  `tests/journeys/.runs/20261011T073549Z/`.
- From `frontend/`: `bun run typecheck`, `bun run lint`, `bun run check:all`
  — passed. Logs: `/private/tmp/evaluation-cleanup-typecheck.log`,
  `/private/tmp/evaluation-cleanup-lint.log`, `/private/tmp/evaluation-cleanup-design.log`.

Manual verification in the existing local project used comparison
`9e1b9caa-858b-48ef-8af6-9e701bd99132`: six model rows, one table, Accuracy,
Cross entropy and Brier, with 625/625 scored per model. Screenshot:
`/private/tmp/evaluation-comparison-cleanup.jpg`. In Eval library, computed fonts
for the exact `Task outcome: Fallback` card and its popup title are Geist Pixel,
weight 400; the Evaluations page title remains PP Mondwest. Screenshot:
`/private/tmp/evaluation-geist-pixel-titles.jpg`.
