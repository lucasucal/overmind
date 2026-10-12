# Evaluation chart layout and hover

Environment: existing local Docker stack, authenticated Console at
`http://localhost:5173`, browser viewport 1280 × 720. No evaluation was launched.

Live fixture: `/evaluations/runs/b7799bbe-d6f0-42b5-899d-f476db238cde?projectId=a279d834-899c-4ac6-888a-157f0c7d9cf8`
(SOC saved-output regrade · closed fallback schema).

Boundary fixture: `/tests/evaluation-charts.html`. Its checked-in HTML/TSX uses
synthetic scores, including 0%, 100%, two evaluators, six model/evaluator series,
and long evaluator names; it makes no API or provider calls.

Browser replay and observed results:

1. Open the live fixture's Scores view. The card has a full-width header divider,
   two 48px rows, names and means above the bars, and only 0%/100% axis labels.
   SVG width is 1164px, exactly the 1166px card width minus its outer borders.
   Plot height is 120px; bars begin at x=0, with y=28/76, height=12 and widths
   62.5%/75%. The mean labels remain 63% and 75%.
1. Point at the second row. At pointer x=900 the vertical guide is also x=900
   and spans the 120px plot. The tooltip reads Jev 75%, mean score, 4 samples.
   It stays within the screen; clicking the plot adds no pointer focus outline.
1. In the boundary fixture's first chart, inspect the first row and press Down:
   the tooltip changes from generative 63% to Jev 75%. Escape removes both tooltip
   and guide. Arrow keys, Home and End inspect the same values as the pointer.
1. In Boundary values, Scores draws widths 0 and 100 rather than fabricating a
   nonzero bar. Box & Whisker retains one visible boundary tick for each series.
1. Select Histogram and press End in the chart. The final 90%–100% bucket reports
   Zero score: 0 samples; Perfect score: 1 sample.
1. Select Distribution and press End. At score 100%, relative densities are
   0.000 and 1.000. Density is labelled separately from sample counts.
1. Select Box & Whisker and inspect Perfect score: minimum, quartiles, maximum
   and mean are all 100%. In Model comparison's Violin view, the first series
   reports minimum 25%, quartiles 44%/81%, median/mean 63%, maximum 100%, based on
   the four retained fixture values [0.25, 0.5, 0.75, 1].

Screenshots (local artifacts): `/private/tmp/evaluation-score-bars.jpg` and
`/private/tmp/evaluation-score-hover.jpg`.

Validation commands from `frontend/`:

```sh
bun run typecheck
bun run lint
bun run check:all
bun run test src/components/evaluations/score-distributions.test.tsx src/components/evaluations/score-distribution-math.test.ts
```

The existing two suites passed all 13 tests. The initial keyboard-chart markup
triggered Biome's noninteractive-tabindex rule; its narrowly scoped suppression
documents the chart's arrow-key application behavior. Formatting and lint were
rerun after the correction. Logs use `/private/tmp/evaluation-chart-final-*.log`.

Evaluation warning banner removal was also checked on the same saved run with
the existing local Docker stack. Open the live fixture URL above and inspect
Results: the evaluator compatibility banner is absent, while the run summary,
63%/75% scores and four per-sample results remain visible. Screenshot:
`/private/tmp/evaluation-without-warning.jpg`. Typecheck, lint and `check:all`
passed again; logs use `/private/tmp/evaluation-warning-*.log`. The test suites
were not repeated for this presentation-only removal.
