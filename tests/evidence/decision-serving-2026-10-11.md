# Automatic Training Deployment

## Environment

- Local Overmind API/MCP: `http://localhost:8000` and `/api/mcp/`.
- Project: `1e3f3e92-b50d-4590-85ed-97921d132d3c`.
- Training experiment: `2729da27-b040-4369-b34b-d8e0f6241e0f`.
- Existing compose Postgres, Redis, API and workers. No new development server.
- Provider environment: `overmind-dev`. No hosted Overmind endpoint was used.
- Local migration `0040_decision_serving` applied successfully; containerized
  `python manage.py makemigrations --check --dry-run` reported no changes.
- The Codex automation `watch-titanic-qwen-size-sweep` remains paused. The local
  Celery scheduler was restarted after its polling timestamps stopped advancing.

## Behavior

Successful native decision training now enters the existing durable deployment
controller instead of finishing without a deployment. The native serving runtime
publishes and verifies the complete adapter/head artifact on the weights Volume.
Readiness requires an actual prediction with the pinned artifact identity and
valid, ordered probabilities. Serving does not mount the training Volume.

REST and MCP share typed durable inference receipts, stable request keys and
project scoping. Decision models reject chat generation and chat alias activation.
Deployment does not change live application routing or benchmark selection.

MCP impact: MCP-ready. Contract 7.1 adds `deploy_finetune` and typed `decisions` to
`run_inference`, with deployment contracts and returned job/resource identifiers.
The generated REST client and native API snippet are updated. Packaged guidance
is versioned with SDK 0.1.88 and skill/plugin 1.2.1; nothing was published to PyPI.

## Local Rollout

Published using `.venv/bin/modal deploy --env overmind-dev PATH`:

| Worker     | Path                                         | Pinned App                                         |
| ---------- | -------------------------------------------- | -------------------------------------------------- |
| Serving    | `overbae/modal/modal_decision_serving.py`    | `overmind-decision-serve-1a9ad6de7ba65600409f2655` |
| Training   | `overbae/modal/modal_sft_worker.py`          | `overmind-sft-58a187580c5d1300d58e3c24`            |
| Evaluation | `overbae/modal/modal_decision_evaluation.py` | `overmind-decision-eval-9e7a3896d39014e59d00387d`  |

The shared release helper changed, so matching training/evaluation releases were
published too. Existing jobs retain their original pinned runtime.

After confirming `list_projects` reported the localhost endpoint, each existing
job was passed to `deploy_finetune` with the explicit project ID above. All three
deployment jobs reached `ready` on attempt 1:

| Model         | Training Job                           | Deployment                             |
| ------------- | -------------------------------------- | -------------------------------------- |
| Qwen 3.5 0.8B | `0309751c-cb28-437e-9abb-bff2a8b88504` | `b670fab7-2a7d-41db-9fa2-38da4d368f9d` |
| Qwen 3.5 2B   | `ebb68626-fccf-41f7-8ad3-1b13e074f7b4` | `f4ccc6be-c339-4962-89f0-2b5f6077a247` |
| Qwen 3.5 4B   | `61d4cbcd-1a5c-4dc2-bff0-4a89f2e4c744` | `69368dfb-e891-4254-8a30-fd329ce8c8f8` |

Public MCP `run_inference` then received each deployment and this input-only
smoke request, without labels or references:

```json
{
  "decisions": [{
    "state": "Serving readiness check.",
    "question": "Select an option.",
    "kind": "choice",
    "options": ["A", "B"]
  }]
}
```

Request keys are `titanic-serving-verification-JOB_PREFIX-20261012`, using the
eight-character training job prefix. Reusing the same key/input recovers the
same request; do not create replacement requests to inspect these results.

| Model | Successful Inference Receipt           | Returned Artifact Identity                                         |
| ----- | -------------------------------------- | ------------------------------------------------------------------ |
| 0.8B  | `5120df38-34c4-4cb7-8af8-fac36dea6969` | `7576666d941dfc5b7e54acca0ac0cf5badc9da63a8cf5b6146b031837bee7df5` |
| 2B    | `78884ce3-40e8-49b3-b2a8-8cb4f610ee40` | `a11eff978ce826dbb905d1a56850631cd155b2102075e24da31197141decb9fa` |
| 4B    | `a8511111-7a05-4cba-bc31-5c9195255cac` | `62e315ad0532f14bf70b1f4425b102362a068181181ad959c84280657ebf4c1f` |

`get_job(kind="inference_request", id=..., project_id=...)` confirmed each
receipt succeeded, retained `["A", "B"]` order, and returned probabilities
from the exact trained artifact. These are readiness smoke calls, not Titanic
quality measurements, calibrated results, performance benchmarks or evidence of
application integration. They are recorded as MCP traffic.

## Automated Verification

```sh
.venv/bin/pytest -n 1 tests/test_model_deployment_resume.py tests/test_mcp_inference.py tests/test_inference.py tests/test_inference_receipts.py tests/test_finetuning_observe.py tests/test_model_swap_prompt.py tests/test_model_activation.py tests/test_mcp_catalog.py -q
```

Result: **143 passed**, 70 existing short-JWT warnings. Log:
`/tmp/decision-serving-verified-tests.log`. Provider calls use network fakes.
Checks cover deployment reconnect/verification, auto-finalization, typed REST/MCP
receipts, input rejection, project isolation, chat compatibility and activation.
An earlier run collided with the journey test database; the final run used the
separate xdist database. An incomplete native test fixture was corrected to
include the required pinned serving environment before this passing run.

```sh
UV_NO_SYNC=1 UV_CACHE_DIR=/tmp/overmind-uv-cache make test-journeys test_args='tests/journeys/test_model_training.py'
```

The Make target included the whole journey directory: **68 passed, 1 failed**.
The trained-model benchmark/serve/activate journey passed. The existing
`test_native_monitoring_evidence_remains_readable_after_cancellation` failed
waiting for the "Development monitoring" heading on the training screen; that
screen was not changed by this inference work. Full receipts and browser evidence
are in `tests/journeys/.runs/20261012T053120Z/`; console output is
`/tmp/decision-serving-journey.log`. This is not an all-green full-suite result.

```sh
TEST_REDIS_URL=redis://localhost:6379/15 .venv/bin/pytest tests/journeys/console/test_console.py -k decision_deployment -q
```

Result: **1 passed, 7 deselected**. This uses the built Console against the
isolated real API with a native deployment fixture. It checks typed submission
and receipt-polling snippets, excludes chat endpoints and live-alias controls,
and records no browser or server errors. Screenshot manually inspected after
waiting for the dialog animation:
`tests/journeys/.runs/20261012T053851Z/decision-inference-snippet.png`.

Frontend `bun run typecheck` and `bun run check:all` passed. The generated OpenAPI
client was regenerated successfully. Scoped pre-commit hooks passed, including
Ruff, Biome and the no-new-internal-test-patches guard. `git diff --check` passed.
