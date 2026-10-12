# Workshop controls on the right

Environment: existing local Docker stack and authenticated Console at
`http://localhost:5173`, browser viewport 1280 × 720.

Fixture: `/datasets/74788292-a65c-43d6-9524-a87d0ab1af03?projectId=a279d834-899c-4ac6-888a-157f0c7d9cf8`.

Browser replay and observed results:

1. Open the fixture. Folder/minimap controls occupy the rightmost 40px of the
   canvas (x=1231–1271); zoom controls sit at x=1237–1265, y=593–699.
1. Show the minimap. Its right edge is x=1223, leaving 14px before the zoom
   controls; the two do not overlap.
1. Expand datasets. The canvas narrows from 1214px to 966px, while its right
   edge and the control rail stay at x=1271. Close datasets again.
1. Click Zoom Out: canvas scale becomes 0.833333. Click Reset view: scale
   returns to 1 with cells clear of the right control rail.
1. Hide the minimap again after verification.

Screenshot: `/private/tmp/workshop-right-controls.jpg` (local artifact).

Validation from `frontend/`, all passed:

```sh
bun run typecheck
bun run lint
bun run check:all
```

Logs: `/private/tmp/workshop-right-controls-{typecheck,lint,design}.log`.
Unit suites were not run for this layout change.
