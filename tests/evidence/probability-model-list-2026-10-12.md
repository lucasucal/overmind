# Probability Inspector Model List

## Scope

The native probability datapoint inspector lists every model vertically in its
right-hand pane, beside the shared frozen input. Model tabs and selection state
are removed. Each section uses the existing read-only model badge, ordered
probability/reference table and aligned score rows. Pending and error states
remain model-specific; no model borrows another model's prediction.

Desktop panes scroll independently. The output list is keyboard-focusable for
scrolling without controls. On narrow screens the input precedes the model list
in the dialog's shared scroll area. Generative inspectors are unchanged.

MCP impact: frontend-only; no API or provider contract changes. No real training,
evaluation or inference was launched.

## Verification

- The existing native benchmark Console journey passed for one, three and six
  participants: **3 passed** in 57.45 seconds.
- No inspector has a model combobox or tab list. All participants render together.
- Ordered original probabilities and soft/hard references remain exact. Pending
  participants show missing probabilities rather than another participant's answer.
- Publishing a prediction through the real monitor service updates the already-open
  model section through polling; other pending sections remain pending.
- Keyboard End/Home scrolls the six-model output list without moving the input.
  Mobile scrolling reaches the final model; panes do not overlap and the dialog
  stays inside the viewport. Escape still restores focus to the datapoint grid.
- Completed ordinal examples retain every model's explicit reference mean, axis
  values and measured expected score.
- Inspected desktop 1440 x 1100 and mobile 390 x 844 screenshots, including the last
  model and completed results. No visual correction was needed.
- Typecheck, design/contrast/control checks, scoped Ruff and Biome checks,
  pre-commit and diff checks passed. Pre-commit's in-place file check required
  an approved retry for the protected `.agents` skill directory.

Artifacts: `tests/journeys/.runs/20261012T063255Z/`, including
`native-benchmark-{1,3,6}-sample-desktop.png`,
`native-benchmark-6-sample-desktop-last-model.png`,
`native-benchmark-6-sample-mobile-last-model.png`, and
`native-benchmark-6-sample-completed-desktop.png`.

Logs: `/tmp/probability-model-list-journey.log`,
`/tmp/probability-model-list-typecheck.log`,
`/tmp/probability-model-list-design.log`, and
`/tmp/probability-model-list-precommit.log`.
