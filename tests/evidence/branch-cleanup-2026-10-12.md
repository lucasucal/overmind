# Decision branch cleanup

The accumulated decision training, native evaluation, serving and Console changes
were committed on `codex/general-decision-training`. Current `origin/main` was
merged without rewriting the published branch history.

## Integration

- Preserved the native Workshop pipeline and evidence model rather than restoring
  retired agent tasks from the old Workshop implementation.
- Combined document-specific upload limits and streaming reads with refreshed
  server-side file stats and offset-based retry-safe chunk writes.
- Adopted request-scoped MCP/OAuth thread and connection cleanup, retaining the
  branch's public auth helpers and both sets of transport tests.
- Kept renewable collector locks with explicit timeouts and retryable renewals.
  Updated the pipeline runner to supply the heartbeat owner required by main.
- Corrected the readiness test's provider fake instead of patching the retired
  chat-only classification path.

## Verification

- Frontend Biome, typecheck and design/contrast/control checks passed.
- Frontend suite: 893 passed across 120 files.
- Backend suite: 4,382 passed, 10 skipped, one heartbeat-call mismatch identified.
  After adding the owner, the complete affected preparation file passed all 13 tests.
- SDK suite: 591 passed. SDK lint and formatting passed.
- Focused live journeys: eight passed, covering renewed-lock recovery, missing-job
  collector shutdown, dataset stream connection release, benchmark monitoring with
  one/three/six models, and training prediction labels.
- Root Ruff lint and formatting passed.
- Migration checks: no model drift; 28 migrations checked, including three retained
  independently committed identities. No migration renumbering was necessary.
- SDK package, module and lock agree on version 0.1.88, above main's 0.1.85.
- Scoped pre-commit checks passed before the initial commit and after merge resolution.

No hosted training, evaluation, inference, deployment or data migration was performed.
