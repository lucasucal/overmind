# Native benchmark monitoring

## Scope

Running native comparisons now expose recorded model stages, prediction coverage,
per-benchmark provisional scores and paginated frozen inputs/references/outputs.
The Console uses the evaluation table and full-size datapoint inspector, with
ordered probability bars and separate calibration/final tabs. Original and
adjusted probabilities remain together; mean-only targets retain their numeric
axis instead of acquiring fabricated probability references.

MCP classification: **MCP-ready** through `inspect_native_evaluation`, contract
7.2.0. REST and MCP share the local indexed projection and project scoping.
The discovery budget increases from 80 to 82 KiB for the added inspection and
native deployment-backfill tools; strict inputs and omitted output schemas remain.

## Verification

- `TEST_REDIS_URL=redis://localhost:6379/15 .venv/bin/pytest tests/journeys/console/test_native_benchmark_monitor.py -q --tb=short`
- `TEST_REDIS_URL=redis://localhost:6379/15 .venv/bin/pytest tests/journeys/console/test_native_benchmark_monitor.py tests/journeys/console/test_console.py::test_evaluations_share_runs_navigation_and_probability_metrics -q --tb=short`
- `.venv/bin/pytest tests/test_native_evaluation_plan.py tests/test_mcp_data_first.py tests/test_mcp_catalog.py tests/test_celery_topology.py -n 1 -q --tb=short`
- `bun run test src/components/model-workflows/workflows.test.tsx src/components/evaluations/confidence-metric.test.tsx src/components/evaluations/runs-table.test.tsx`
- `bun run typecheck`, `bun run check:all`, generated OpenAPI client and scoped pre-commit.

The live-stack journey uses local Postgres, Redis, ASGI, Celery and a built Console.
Only the Modal boundary is faked. Three frozen participant identities, 28 inputs,
hard and soft categorical references, and a mean-only ordinal reference exercise:

- Startup stages before any predictions; metrics after the first two results.
- Repeated observations without duplicate scoring or provider submissions.
- Exact row zero and independent missing outputs for another selected model.
- Rejection and recovery of a corrupt progress chunk without failing inference.
- Separate metric denominators; no cross entropy for mean-only references.
- Paginated sample inspection through REST and MCP.
- Complete collection/scoring followed by local-only historical index rebuild.
- The selected model persists while the inspector polls.
- Desktop 1440x1100 and mobile 390x844, with keyboard row activation and bounded
  dialog geometry; no page overflow, page errors, server errors or execution buttons.

Two combined Console journeys passed; the final polling/aggregation journey passed
again. Focused backend checks: 31 passed. Frontend checks: 17 passed.
MCP catalogue, response compatibility and transport checks: 18 passed, including
the read-only inspection contract and bounded manifest. Scoped pre-commit,
typecheck, design/contrast/control guards and `git diff --check` passed.
Logs are `/tmp/native-monitor-journey-final.log`,
`/tmp/native-monitor-journey-poll.log`, `/tmp/native-monitor-backend.log` and
`/tmp/native-monitor-frontend.log`.

Visual evidence: `tests/journeys/.runs/20261012T055824Z/`, files
`native-benchmark-running-{desktop,mobile}.png` and
`native-benchmark-sample-{desktop,mobile}.png`, with matching browser receipts.
Tables retain their own horizontal scroll on narrow screens.

## Local Titanic Verification

Project `1e3f3e92-b50d-4590-85ed-97921d132d3c`, evaluation
`7b406fc7-2e86-4dbf-8446-17ff7fd3ecf6` was inspected through localhost MCP.
All three models have 89/89 final and 89/89 calibration samples indexed. Sample
`0` retains both original and adjusted two-option distributions for all three.
No training, evaluation, activation or inference run was started for verification.

Worker `overmind-decision-eval-fe970270dc628bb4c3488a85` was deployed to the
configured `overmind-dev` Modal environment. This publishes code only. Future
plans pin this release; historical plans retain their original release and do
not acquire invented live telemetry. No new paid GPU run was used to validate
publication; progressive collection was verified at the provider boundary.

## Boundaries

Worker chunks carry exact call, runtime, artifact and input identities, row
counts and checksums. Reference values remain local. Monitoring publication or
indexing failure stays separate from benchmark failure and never replays a call.
Provisional scores are not final paired rankings or checkpoint-selection evidence.
