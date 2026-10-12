# Workshop Process control removal

Environment: existing local Docker stack, authenticated Console at
`http://localhost:5173`.

Browser replay: open `/datasets/74788292-a65c-43d6-9524-a87d0ab1af03?projectId=a279d834-899c-4ac6-888a-157f0c7d9cf8`
and inspect the header and loaded preparation canvas.

Observed: no Preparation details/Process button; one Switch dataset control.
The original source and Build survival decision examples cells render with their
recorded connection, script disclosure and data table.

Screenshot: `/private/tmp/workshop-without-process.jpg` (local artifact).

Validation from `frontend/`: `bun run typecheck`, `bun run lint`, and
`bun run check:all`. Logs: `/private/tmp/workshop-remove-process-{typecheck,lint,design}.log`.
Unit suites are omitted for this UI removal.
