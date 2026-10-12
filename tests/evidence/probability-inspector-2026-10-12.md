# Probability Datapoint Inspector

## Scope

Presentation-only refinement of `SampleInspector` in
`frontend/src/components/evaluations/probability-evaluation-monitor.tsx`.
The model dropdown is removed. Multiple models use the existing generative
inspector's tabs; a single model has no switching control. Compact pane headers,
a read-only model badge, full-width shared table rows and aligned score rows
replace the inset probability bars and loose metric footer.

Original option order, references, original/adjusted probability columns,
mean-only targets and missing-output states remain supported. No execution
buttons, platform operations, evaluation launches or serving changes were added.
MCP impact: frontend-only, unchanged read contract.

## Verification

- The existing live Console journey now runs with one and three participants:
  **2 passed** in 26.94 seconds.
- Keyboard opening, arrow-key model switching, End-key access to the last model
  on mobile, selection persistence during polling and missing-model outputs pass.
- The single-model dialog contains neither a combobox nor model tabs.
- Exact ordered probabilities and reference percentages are asserted in the table.
- Desktop 1440 x 1100 and mobile 390 x 844 screenshots were inspected. Mobile
  panes do not overlap, the dialog stays within the viewport, and the standard
  three-column option/probability/reference table fits without horizontal scrolling.
- Existing incremental metrics, receipt validation and completed-run backfill
  checks still pass. Provider calls use the journey's network fake; no real
  training or evaluation was started.
- Typecheck, design/contrast/control checks, scoped pre-commit and diff checks pass.

Artifacts: `tests/journeys/.runs/20261012T061631Z/`, including
`native-benchmark-{1,3}-sample-desktop.png` and
`native-benchmark-{1,3}-sample-mobile-output.png`.

Logs: `/tmp/probability-inspector-journey-final.log`,
`/tmp/probability-inspector-typecheck.log`,
`/tmp/probability-inspector-design.log`, and
`/tmp/probability-inspector-precommit.log`.
