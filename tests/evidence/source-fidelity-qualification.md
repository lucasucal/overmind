# Source fidelity — Package B qualification

Revision: `codex/source-fidelity` @ `f62bb282674291d720deaa87210f77601acfa74a`.
Date: 2026-10-12.
Surfaces: MCP `overmind://dataset-upload`, `overmind://interface/current`, `inspect_dataset`, `get_job(dataset_run)`; CLI upload; REST transfer inspect; cell export JSONL.
Console extraction UI is dispositioned MCP-native (`source-fidelity-contract-review.md`); not re-checked.

Companion: `source-fidelity-qualification.json`.
Single live log: `/private/tmp/source-fidelity-pkgb-replay-full.log` (sha256 `9112fef679fa…`).
No paid providers. `billable_usage_records: 0`.

This pass is one execution of 26 cases. Earlier split logs are not this result.

## Labelling

| Evidence                                             | Kind                                                      | What it covers                                                 | What it does not                    |
| ---------------------------------------------------- | --------------------------------------------------------- | -------------------------------------------------------------- | ----------------------------------- |
| This live replay                                     | THIS REVISION, live, one run                              | 26 landing/refusal cases on hashed fixtures                    | Not pytest, not journeys            |
| Host pytest 137 passed                               | THIS REVISION, pytest / in-process MCP                    | Documents, transfers, scalars, JSON field, MCP resource fields | No HTTP MCP, no 2000-page live file |
| `make test-journeys -k data_workshop` 21 passed      | THIS REVISION, journeys (provider-faked; extraction real) | Source filter vs destination; repeated invocations             | No PDF/OCR matrix                   |
| TradingAgents Pi read of `overmind://dataset-upload` | THIS REVISION, live HTTP MCP                              | Numeric limits and limitation prose                            | Does not land files                 |
| `workshop-pdf-experience.md` (2026-10-08)            | PRIOR REVISION, live                                      | Earlier PDF replay                                             | Not this revision                   |

Do not add these counts together.

## Live cases

26 passed, 0 failed, one process.

Independent comparison for landed PDFs: original-byte SHA download, per-page markers and `document_id` on every exported JSONL row, provenance regions on every exported row. MCP `query_dataset` is not used as the provenance source (32 KiB cap).

`document_and_ocr_evidence_round_trip` includes `scan-rotated.jpg` (pixels rotated 90°, EXIF orientation 6) and asserts `coordinate_space == exif-oriented-pixels`. `rotated-native.pdf` only sets PDF `/Rotate` on native text; that is not raster/EXIF proof.

`pdf_over-byte-limit` refused with `overmind://dataset-upload` in the SDK error, `uploaded_bytes: 0`, and no PUT on the SDK session. Extra POST/GET from connection check are expected.

`semantic_quality` is not reported on landing cases. There is no pipeline receipt on this path.

## Discovered limits (live MCP)

`overmind://interface/current` contract_version `7.3.0`.

| Field                  | Observed   |
| ---------------------- | ---------- |
| `document_max_bytes`   | 104857600  |
| `pdf_max_pages`        | 2000       |
| `json_array_max_bytes` | 268435456  |
| `max_bytes`            | 2147483648 |
| `chunk_bytes`          | 8388608    |
| `max_files`            | 100        |

`documents` prose: 100 MiB per document, 2000 pages per PDF, 64 megapixels, animated images rejected, English Tesseract, reading order not reconstructed.
`json_selection`: JSON object requires `--json-rows-field`; wrapper keys are not guessed.
Missed text is not semantic success: recovery does not certify partial omissions; `mixed-blank-pages.pdf` records `Pages without extracted text: 3, 6`.

## Reproduction

Compose stack already running. Fixture generation needs ReportLab, pypdf, Pillow on the host. Checkout `f62bb28` for the harness used in this log. Tesseract 5.5.3 (`eng`, `osd`).

```sh
git checkout f62bb282674291d720deaa87210f77601acfa74a
pdf_fixture_dir=$(mktemp -d /private/tmp/workshop-pdf-fixtures.XXXXXX)
uv run --with reportlab --with pypdf --with pillow python tests/evidence/workshop_pdf_fixtures.py "$pdf_fixture_dir"
pdf_replay_dir=$(docker compose exec -T api mktemp -d /tmp/workshop-pdf-replay.XXXXXX)
docker compose cp overmind/overmind "api:$pdf_replay_dir/overmind"
docker compose cp tests/fixtures/documents "api:$pdf_replay_dir/documents"
docker compose cp "$pdf_fixture_dir" "api:$pdf_replay_dir/pdfs"
set -o pipefail
docker compose exec -T -e PYTHONPATH="$pdf_replay_dir" -e DO_NOT_TRACK=1 \
  -e WORKSHOP_ACCEPTANCE_PDFS="$pdf_replay_dir/pdfs" \
  -e WORKSHOP_ACCEPTANCE_DOCUMENTS="$pdf_replay_dir/documents" \
  -e WORKSHOP_ACCEPTANCE_CASES='catalogue_auth_and_all_tool_validation,tabular_file_upload_transform_export,document_and_ocr_evidence_round_trip,pdf_native-1,pdf_native-10,pdf_native-100,pdf_native-500,pdf_native-2000,pdf_native-2001,pdf_scanned-1,pdf_scanned-25,pdf_mixed-30,pdf_rotated-native,pdf_mixed-blank-pages,pdf_large-scanned,pdf_near-byte-limit,pdf_over-byte-limit,pdf_encrypted,pdf_blank,pdf_corrupt,pdf_batch_10,pdf_batch_25,pdf_batch_100,pdf_mixed_batch,pdf_atomic_batch_recovery,pdf_batch_limit_101' \
  api python manage.py shell < tests/evidence/workshop_mcp_acceptance.py \
  2>&1 | tee /private/tmp/source-fidelity-pkgb-replay-full.log
```

Fixture hashes: `source-fidelity-qualification.json`.

## Follow-on: messy report PDF

Separate from the 26-case run. One extra live case `pdf_messy-report` after adding `messy-report.pdf` (title, 4-row SKU grid, two-column notes, second page footer).

Log: `/private/tmp/source-fidelity-messy-report.log` (sha256 `faaf69f98dcc…`). Passed in 0.796 s. 2 pages, 25 exported rows, original-byte SHA `fda74fdaab75fa35eb6dc50926ae582f2950eb182464ba11349841ee06c5dba7`. Extraction `docling-native-pdf` 2.131.0. Limitation retained: `Reading order and visual table structure are not reconstructed.`

Phrases found in exported row text: `Q3 warehouse exception log`, `Returns window is thirty days from delivery`, `SKU-4419`, `SKU-8821`, `Aisle B7 is closed on bank holidays`, `Cycle count 8841`, `HOLD-ZONE-C`.

This does not reconstruct a table, score layout, or claim semantic quality.

```sh
pdf_fixture_dir=$(mktemp -d /private/tmp/workshop-pdf-fixtures.XXXXXX)
uv run --with reportlab --with pypdf --with pillow python tests/evidence/workshop_pdf_fixtures.py "$pdf_fixture_dir"
pdf_replay_dir=$(docker compose exec -T api mktemp -d /tmp/workshop-pdf-replay.XXXXXX)
docker compose cp overmind/overmind "api:$pdf_replay_dir/overmind"
docker compose cp "$pdf_fixture_dir" "api:$pdf_replay_dir/pdfs"
docker compose exec -T -e PYTHONPATH="$pdf_replay_dir" -e DO_NOT_TRACK=1 \
  -e WORKSHOP_ACCEPTANCE_PDFS="$pdf_replay_dir/pdfs" \
  -e WORKSHOP_ACCEPTANCE_CASES='pdf_messy-report' \
  api python manage.py shell < tests/evidence/workshop_mcp_acceptance.py \
  2>&1 | tee /private/tmp/source-fidelity-messy-report.log
```

## Limits of this proof

Handwriting, multilingual OCR, table reconstruction, cancellation during PDF OCR, worker restart during large landing, and an exact 100 MiB boundary file were not added. A 2-page grid/two-column report was landed for phrase presence only. `near-byte-limit.pdf` landed; `over-byte-limit.pdf` was refused with no SDK PUT.
Pipeline package execution is out of this package. Image 64MP / animated rejection remain pytest and MCP prose, not this 26-case list.
The 2026-10-08 PDF replay is prior-revision evidence.
