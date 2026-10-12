# Probability Datapoint Search and Filters

## Scope

The native benchmark datapoint table has shared Console search, model and outcome
selectors, plus clear-filter and no-result states. Search matches input text,
source keys and benchmark names in the full saved suite before pagination. Model
selection narrows visible prediction columns and scopes outcome matching. With
all models selected, any participant may match the requested outcome.

Correct/incorrect use recorded raw accuracy only; soft distributions and ordinal
means are not treated as hard answers. Missing output and unscored evidence have
separate filters. Aggregate model metrics stay unfiltered. Filter changes reset
pagination, live result-count reductions clamp the current page, and switching
runs resets filter state. Exact-row inspection is independent of table filters.

REST and MCP use the same parameterized SQLite query over retained evidence, with
one read snapshot for counts and rows. MCP-ready: contract 7.3.0 exposes the same
optional search, participant and outcome arguments through
`inspect_native_evaluation`. Exact keys cannot be combined with filters. The
generated OpenAPI client was regenerated through the repository command.

## Verification

- Console journeys for one, three and six models, plus MCP catalog/manifest checks:
  **17 passed** in 73.93 seconds.
- Checked full-suite search beyond the current page, combined model/outcome/text
  filters, pagination reset, clear search/filters, no-result recovery and exact-row
  opening from a filtered table.
- REST and MCP agree on filtered counts and sample identities. Unknown models and
  outcomes, and conflicting key/filter requests, are rejected. Literal SQL-like
  strings, `%` and `_` do not act as query syntax or wildcards.
- Partial missing predictions and completed outcomes are distinguished. Soft and
  ordinal examples are excluded from correct/incorrect filters. Aggregates remain
  identical before and after filtering; reads do not create provider calls.
- Inspected dark desktop 1440 x 1100 and mobile 390 x 844 filter-toolbar captures.
  Controls wrap without page overflow; standard table scrolling is retained.
- Typecheck, design/contrast/control checks and scoped pre-commit passed.

The first test exposed participant-variable shadowing in the read service; this
was corrected before the passing run. The browser test also corrected its expected
pagination label to the shared component's singular `row` form.

Artifacts: `tests/journeys/.runs/20261012T065528Z/`, especially
`native-datapoint-filters-{1,3,6}-{desktop,mobile}.png`.

Logs: `/tmp/probability-filter-journey-final.log`,
`/tmp/probability-filter-typecheck.log`, `/tmp/probability-filter-design.log`,
`/tmp/probability-filter-client.log`, and `/tmp/probability-filter-precommit.log`.

All model calls use the journey's network fake. No real evaluation, training,
deployment, routing change or scheduled task was started.
