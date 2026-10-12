# Training prediction labels

Decision training now shows ordered label chips alongside Dataset in the existing
run metadata. Shared pinned cells appear once across variants. Score axes keep
their declared values; zero-probability options remain present. Missing data and
launch-identity conflicts are unavailable rather than inferred.

The agreed layout removes the standalone section, icon, categorical tint and label
count. Neutral chips match the existing metadata surface. Single questions remain
accessible/hover context; multiple questions and datasets keep their own captions.
The journey checks metadata placement, absence of the removed decoration, chip
overflow and retained label order. Single-job retrieval now maps its recorded
training contract into the list shape so native labels render without a group.

## Contract and scope

- MCP-ready: REST detail and the existing MCP finetune resource share
  `record.prediction_labels` through `run_record`. The compact `get_job` receipt
  links to that resource. No new operation or provider call is introduced.
- The existing generated frontend client consumes the JSON record. No endpoint,
  schema, migration, dependency or generated-client change is needed.
- Full pinned-cell verification and distinct-label projection are cached by cell,
  checksum and file stat. Return limits are eight complete sets and 12 KB; total
  set count remains explicit, and labels are never truncated.
- The original training version is used even when the dataset has a newer version.
  No training, evaluation or inference job was started for verification.

## Verification

- `bun run typecheck`: passed.
- `bun run check:all`: passed.
- Focused training-monitor and platform-qualification Vitest files: 27 passed.
- Metadata refinement: training-monitor and run-query Vitest files: 26 passed.
- `tests/journeys/console/test_training_labels.py`: 1 passed. Exercises REST and
  MCP consistency, newer active data, zero-probability labels, shared/focused/single views,
  ordinal means, long labels, bounded coverage, missing cells, launch mismatch and
  absence on chat jobs. Earlier failures were corrected test fixtures/selectors.
- Existing MCP finetuning/resources and training-runs API tests: 107 passed,
  1 failed. `test_readiness_classifies_selected_capability_and_defers_to_data_for_none`
  expects `code_generation` but gets `classification`; its readiness path does not
  call the changed run-record code. The later branch cleanup corrected its fake
  provider setup for both typed decisions and the chat fallback; the focused
  Redis-backed check and the full backend run now pass that test.
- Impeccable detector: no findings for the new component.

Playwright screenshots were inspected at desktop 1440x1100 and mobile 390x844.
Labels fit without overlap or document overflow, including a 150-character option.
Metadata-layout artifacts are under `tests/journeys/.runs/20261012T074042Z/`:

- `training-prediction-labels-desktop.png`
- `training-prediction-labels-mobile.png`
- `training-prediction-labels-single-mobile.png`
- `training-prediction-labels-varied-mobile.png`
