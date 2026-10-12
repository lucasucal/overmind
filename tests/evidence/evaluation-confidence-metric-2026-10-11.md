# Separate evaluation confidence metric

## Behaviour

- Removed the Raw/Calibrated view switch from native evaluation results.
- Added a Confidence card alongside the existing evaluation metrics. Each model shows observed correctness and claimed confidence, with a hatched gap and a confidence marker. Original and adjusted results appear together when both were recorded.
- Soft or mixed probability references are labelled Reference support, never Correct. Mean-only references do not produce a confidence bar.
- Summaries weight the retained reliability bands by their decision counts. Invalid or denominator-mismatched evidence is omitted. The view uses final evaluation evidence, not in-sample calibration results.
- Calibration error averages absolute gaps within the recorded confidence bands. It appears beside each bar and as a sortable comparison-table metric. This prevents whole-run average cancellation from being mistaken for good calibration.
- Main score charts and table values remain the original scores. Table tooltips retain adjusted scores and their denominators. The training result panel uses the same confidence card.
- The existing bands cannot isolate an exact 90%+ subset, so the card explicitly reports all measured probability-labelled decisions instead of inferring that subset.

## Local verification

Inspected the existing completed `Titanic survival before-after native decision benchmark` evaluation (`aeecf56c-6407-4989-bc1f-fd4bc2e6f79c`) in the localhost Console. It has 89 final decisions and a separate 44-row calibration dataset.

| Model                 | Probabilities | Correct | Claimed | Calibration error |
| --------------------- | ------------- | ------- | ------- | ----------------- |
| Qwen3 0.6B foundation | Original      | 61.8%   | 50.3%   | 11.5 pp           |
| Qwen3 0.6B foundation | Adjusted      | 61.8%   | 60.3%   | 2.1 pp            |
| Titanic survival LoRA | Original      | 80.9%   | 79.9%   | 7.3 pp            |
| Titanic survival LoRA | Adjusted      | 80.9%   | 80.9%   | 10.0 pp           |

The last row demonstrates why matching overall confidence and correctness must not replace the banded calibration error. The Brier chart retained the original scores, 0.4985 and 0.3092. Verified both probability views are simultaneously visible with no Raw/Calibrated toggle and no browser console errors.

Screenshot: `/private/tmp/evaluation-confidence-metric.jpg`.

## Automated checks

- Confidence summary/rendering, comparison integration, and training result tests: 10 passed across three files. Cases cover unequal bin weights, cancelling errors, soft labels, invalid/missing evidence, both probability views, and retained adjusted-score details.
- Frontend typecheck, Biome lint, and design/contrast/control checks passed.

No backend or MCP contract changed. Both already expose the retained reliability evidence used by this presentation. Verification read saved local evaluations; it did not launch training, evaluation, inference, or provider work.
