# Model Comparison Table

## Change

`ComparisonMetrics` now uses the shared Console DataTable, matching the
probability datapoints list. It has compact model/baseline badges, bounded
resizable columns and the shared ascending/descending/reset header sorting.
Benchmark groups remain intact while rows sort within each group.

Scores keep their native units and measured coverage. Link-like dotted
underlines and permanent direction arrows are removed. Score tooltips retain
denominators, intervals, paired differences and adjusted values. Incomplete
coverage shows a warning glyph next to the count; hover or focus reveals the
exact missing, invalid and incompatible counts.

The existing table-sort hook exposes its state setter so the shared header's
reset state can reuse the same missing-values-last sorting implementation.
No backend or MCP contract changed; no model execution was started.

## Verification

- Four Console journeys passed in 49.67 seconds: one-, three- and six-model
  benchmark flows, plus evaluation navigation and coverage-warning inspection.
- Comparison headers cycle through all three sort states. The full table
  remains available without pagination; benchmark membership is retained.
- Desktop and mobile screenshots were inspected, including long model names,
  soft/hard target metrics, ordinal targets and the rightmost mobile columns.
- Twenty-six focused frontend tests passed across workflow rendering, table
  sorting and shared DataTable accessibility. Adjusted score tooltips and
  coverage-warning keyboard access are covered.
- Typecheck, design/contrast/control checks, scoped pre-commit and diff checks pass.

Artifacts: `tests/journeys/.runs/20261012T062736Z/`, including
`native-model-comparison-{1,3,6}-desktop.png`,
`native-model-comparison-{1,3,6}-mobile.png`, and
`native-model-comparison-{1,3,6}-mobile-metrics.png`.

Logs: `/tmp/model-comparison-journey.log`,
`/tmp/model-comparison-frontend-final.log`,
`/tmp/model-comparison-typecheck.log`,
`/tmp/model-comparison-design.log`, and
`/tmp/model-comparison-precommit.log`.
