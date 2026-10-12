# Bounded Workshop script viewer

Environment: existing local Docker stack, Console at `http://localhost:5173`,
authenticated local project `a279d834-899c-4ac6-888a-157f0c7d9cf8`.

Fixture: dataset `74788292-a65c-43d6-9524-a87d0ab1af03`, cell
`c1130b35-57b3-4d7b-a1fa-6f90696d05d5` (Build survival decision examples),
67-line `transform.py`, revision 1, 891 output rows.

Repeat in the Console:

1. Open the fixture dataset and expand Script. Pan the canvas so the script and
   Data header are both visible.
1. Scroll inside the script. The code and line numbers move together; the file
   controls, Data header and canvas stay in place.
1. Open Package files. Focus the retained source viewer and press End to reach
   its final lines.

Observed through browser DOM measurements and native input:

- Both script views: client height 320px, scroll height 1340px.
- Wheel input moved the step script from scrollTop 0 to 576px.
- Keyboard End moved retained source from scrollTop 0 to its 1020px maximum.
- Canvas transform remained `translate(-2340px, -523px) scale(1)` during both.
- The Data section remained below the bounded viewer.
- Screenshot: `/private/tmp/workshop-script-scroll.jpg` (local verification artifact).

Validation commands from `frontend/`, all passed:

```sh
bun run typecheck
bun run lint
bun run check:all
```

Logs: `/private/tmp/workshop-script-scroll-{typecheck,lint,design}.log`.
Unit suites were not run for this presentation-only change.
