# Probability Datapoints Table

## Change

The native benchmark datapoints list now uses the shared Console DataTable.
It replaces the custom two-line rows with compact state previews and inline
prediction/probability pairs. Model headers use read-only provider badges;
columns resize and retain their widths per run. The standard footer owns
pagination. Row navigation uses the shared roving keyboard focus and active tint.
Closing the inspector explicitly returns focus to the table's focused row.

The full question/state remain in the input preview title and existing inspector.
Probabilities remain neutral values, not accuracy scores. Pending, absent and
unscored outputs stay distinct. Participant column IDs are namespaced so a model
key such as `input` cannot collide with a fixed column.

No sorting of partial pages, backend changes, model execution or new execution
actions were added. MCP impact: frontend-only; the read contract is unchanged.

## Verification

- Console native benchmark journey: **3 passed**, covering one, three and six
  participants. Verified compact rows, one keyboard entry point, arrow navigation,
  row opening/highlighting, focus return, model tabs and polling persistence.
- Verified page two opens the correct retained sample, column dragging persists
  a width, and the last model can be reached by horizontal scrolling on mobile.
- The existing evaluation-navigation/metrics Console journey also passed with
  the shared empty state replacing an empty table.
- Existing frontend workflow and DataTable accessibility suites: **24 passed**.
- Typecheck, design/contrast/controls checks, scoped pre-commit and diff checks pass.
- Desktop 1440 x 1100 and mobile 390 x 844 screenshots were inspected. The tests
  use the real local API/worker flow with network-faked provider calls; no live
  training or benchmark was launched.

The first test pass exposed an overly strict row-height assertion and a real
focus-return defect. The assertion now allows the shared table's 33px rows;
the focus defect is fixed and covered by the passing journey.

Artifacts: `tests/journeys/.runs/20261012T062316Z/`, including
`native-datapoints-{1,3,6}-completed-desktop.png` and
`native-datapoints-{1,3,6}-table-mobile.png`. Mobile images show the visible scroll
region; assertions separately verify access to the rightmost model column.

Logs: `/tmp/datapoint-table-journey-focus.log`,
`/tmp/datapoint-table-journey.log` (navigation pass and initial density failures),
`/tmp/datapoint-table-frontend.log`, `/tmp/datapoint-table-typecheck.log`,
`/tmp/datapoint-table-design.log`, and `/tmp/datapoint-table-precommit.log`.
