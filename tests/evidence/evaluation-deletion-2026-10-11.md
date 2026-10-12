# Evaluation selection and deletion

## Completed behaviour

- Both generated-response and decision rows have selection checkboxes and a Delete action in the common Runs table.
- Single deletion retains the existing undo window. A failed commit restores the hidden row.
- Selection retains each run's ID and format across pages. Select-all affects the current page without dropping other selected pages. Format-qualified keys prevent collisions between the two tables.
- Bulk deletion awaits every outcome, clears and hides successes, and keeps failures selected for retry. Errors are surfaced once; concurrent mutation callbacks cannot strand the bulk operation.
- The generated client dispatches each format to its own deletion endpoint and refreshes the run list, dataset facets and cached details.

## Decision lifecycle

`DELETE /api/native-evaluations/{id}/` uses the shared service and a row lock. It records `deleted_at`, removes the evaluation from Console/REST/MCP lists, and rejects active or unresolved work. An unfinished evaluation needed by a training experiment cannot be removed. Repeating a successful deletion is idempotent.

Training references, provider receipts, report artifacts, prediction-reuse references and request-key identities remain retained. Recorded results remain inspectable by their existing internal references. A deleted request key cannot dispatch a replacement evaluation, and deleted evaluations cannot launch, resume or prepare. Previously queued tasks and the reconciler do not restart them. Training polling stops for a deleted evaluation while continuing for an unfinished training job.

MCP impact: deletion itself is **out of scope** for the public MCP catalogue because this change completes the Console's destructive run-management action. MCP listings reflect removal, retained receipts expose `deleted_at`, and deleted evaluations offer inspection rather than execution actions. Existing dependency reads remain available.

## Verification

- 60 backend tests passed across deletion, unified activity, native evaluation lifecycle, MCP research workflows and performance workflows.
- 20 frontend tests passed across table interactions, mutation routing, training polling and the native evaluation panel.
- Typecheck, lint, design/contrast/control checks and migration validation passed.
- Migration `0039_native_evaluation_deletion` was applied to the local development database; the OpenAPI client was regenerated.
- In the local Jev validation project's six-row mixed list, verified all six checkboxes, per-row delete buttons and the bulk confirmation. Cancelled the confirmation and cleared selection. No existing run was deleted and no provider work was launched.

Screenshot: `/private/tmp/evaluation-selection-and-delete.jpg`.
