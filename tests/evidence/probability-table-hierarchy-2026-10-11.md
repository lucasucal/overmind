# Probability Table Hierarchy

## Change

The benchmark datapoint grid separates reference targets, correctness and model
probability. The reference column shows the actual single-answer target, a soft
target chip with its full distribution on hover, or an explicit ordinal mean.
Predictions use the shared semantic success/check and error/cross chips only when
the retained raw accuracy metric is 1 or 0. Soft and ordinal examples stay neutral.
Reported probability is numeric with a neutral magnitude bar, not a correctness
threshold. A compact legend names the outcome colors and probability bars.

Pending, absent and unscored outputs retain distinct labels and icons. Tied maxima
are explicit in accessible labels and tooltips, consistent with the scorer's
first-option tie break. Full labels remain available when columns are truncated.
Shared chip sizing keeps rows stable as predictions arrive. Existing pagination,
resizing, row keyboard navigation and the all-model inspector remain unchanged.

MCP impact: frontend-only; no API changes or real model execution.

## Verification

- The local Console journey passed for one, three and six participants:
  **3 passed** in 57.55 seconds, using network-faked provider calls.
- Verified stored correct/incorrect scores drive chip colors. A 90% wrong answer
  is red; a correct 50.1% answer is green with a separate probability bar.
- Soft references retain both 70% and 30% in the tooltip, without pass/fail
  coloring. Ordinal reference mean 7 remains neutral. Tied maxima stay explicit.
- Verified consistent row heights, live updates, keyboard navigation, inspector
  focus return, column resizing, pagination and horizontally scrolling model cells.
- Inspected dark desktop 1440 x 1100 and mobile 390 x 844 screenshots of pending
  and completed tables. No page overflow or overlapping cell contents.
- Typecheck, design/contrast/control checks and scoped pre-commit passed.

The first check exposed row-height differences between pending and populated
predictions. Shared chip sizing resolved them. The height assertion also allows
the shared table's borderless last row to be one pixel shorter.

Artifacts: `tests/journeys/.runs/20261012T064131Z/`, including
`native-datapoints-6-completed-desktop.png`,
`native-datapoints-6-completed-mobile-predictions.png`, and
`native-datapoints-3-table-desktop.png`.

Logs: `/tmp/probability-hierarchy-journey-final.log`,
`/tmp/probability-hierarchy-typecheck.log`,
`/tmp/probability-hierarchy-design.log`, and
`/tmp/probability-hierarchy-precommit.log`.
