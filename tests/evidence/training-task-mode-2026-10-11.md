# Training task and mode

Failure cases checked before implementation:

- Native decision format replaces an established semantic task with `decision`.
- Chat-shaped heuristics infer extraction or question answering from native rows.
- A missing task classification is presented as a known capability classification.
- Changing the task label accidentally broadens the native model catalogue.
- Native tasks receive chat benchmark grades or invoke dataset rubric generation.
- Chat training task classification changes when the native branch is corrected.

The existing native CLI/REST/MCP/Console journey covers unknown and stored semantic
tasks, the decision training contract and restricted model catalogue. The isolated
recommendation cases cover semantic versus heuristic context and an explicitly
selected capability; those branches are not covered by that journey.

## Environment and commands

Local Docker Postgres/Redis and hot-reloading API/Console; Bun and uv with the
repository test dependencies. Journeys use isolated test data and fake providers.

```sh
uv run pytest -q tests/test_recommendation_engine.py tests/test_mcp_finetuning.py
make test-journeys test_args='-k test_decision_data_selects_native_training_controls'
cd frontend
bun run test src/components/finetuning/train/__tests__/models-panel.test.tsx
bun run typecheck
bun run lint
bun run check:all
```

## Observed results

- The three new native recommendation cases failed before the fix: each returned
  `decision` instead of the semantic task or `unknown`.
- After the fix: 84 backend/MCP tests, 9 frontend tests and the focused journey
  passed. Typecheck, lint and design/contrast/control checks passed.
- The repository test-seam check rejected internal mocks in the new regression
  cases. They now call the real classifier through the existing fake provider;
  all three cases passed again (`training-task-provider-test.log`).
- An initial journey command supplied a file selector alongside the Make target's
  directory, collecting more journeys than intended. It was interrupted after
  four passes and replaced with the filtered command above, which passed one
  journey with 67 deselected. Logs: `/private/tmp/training-task-*.log`.
- The focused journey's retained JSON and screenshot are under
  `tests/journeys/.runs/20261011T071703Z/`, named
  `tests_journeys_console_test_console.py_test_decision_data_selects_native_training_controls`.
- The journey uploads 12 native refund examples, verifies unknown task through
  REST and MCP, records a semantic classification fixture, and verifies
  `classification` on both surfaces and in the Console. Its native model catalogue
  remains restricted and no training job is created.
- Local smoke check: project `e18b29b5-915d-45a7-80cd-77ffe6559205`, dataset
  `369b56c9-3f77-48a6-8c5c-5aa7f217b602` (`sample_10000.json`), cell
  `8de529f5-9d5b-45eb-96ef-5186462549f5`. Open
  `http://localhost:5173/training?projectId=e18b29b5-915d-45a7-80cd-77ffe6559205&train=true&datasetId=369b56c9-3f77-48a6-8c5c-5aa7f217b602`.
  It displays Training mode: Decision, Task type: Not classified, 404 rows,
  approximately 432k tokens, and the unchanged 323/81 split. Screenshot:
  `/private/tmp/training-task-mode.jpg`.
- Local MCP `check_finetune_readiness` with that explicit project/dataset and
  `eval_model_before=false`, `eval_model_after=false` returns unknown task, a valid
  decision format, `decision_cross_entropy`, typed probability inference and
  29 eligible models. No training or evaluation was launched.

MCP impact: corrected task metadata and removed model eligibility's dependency on
that label. The existing training contract remains the authority for training
mode. No endpoint, input/output field or generated client schema changed.
