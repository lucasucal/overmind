# Clickable table headers

Data-column headers toggle ascending and descending ordering through the shared
header controls. Action columns retain their controls. Local tables preserve
sections and summary rows; paginated lists order matching records before paging.
Training runs and observability conversations remain whole when reordered.

## Verification

- Frontend: 118 test files, 874 tests passed.
- Targeted API suites: training runs, unified evaluation activity, inference,
  billing and task executions passed. Regression cases cover whole-run paging,
  missing durations, visible run names, median inference metrics, billing labels
  and grouped/ungrouped usage ordering. Trace usage aggregation also passed.
- TypeScript, Biome lint, design, contrast and control checks passed.
- Local Console: Training Duration sorts 2m43s before 47m42s ascending, reverses
  with Enter, and retains the unmeasured run last in both directions.
- Local Console: Evaluations Variants sorts 1, 2, 6 across generative and decision
  runs. The model comparison Cross entropy header sorts the six retained models
  numerically ascending and descending. No jobs were launched.

Screenshots: `/private/tmp/table-sorting-training.jpg` and
`/private/tmp/table-sorting-comparison.jpg`.

MCP impact: no tool contract changes. This adds Console ordering and corresponding
REST query support; it does not change stored training/evaluation measurements.
