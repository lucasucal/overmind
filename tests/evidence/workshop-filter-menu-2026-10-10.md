# Workshop filter menu styling

Environment: existing local Docker stack and authenticated Console at
`http://localhost:5173`.

Fixture: `/datasets/74788292-a65c-43d6-9524-a87d0ab1af03?projectId=a279d834-899c-4ac6-888a-157f0c7d9cf8`,
Build survival decision examples cell `c1130b35-57b3-4d7b-a1fa-6f90696d05d5`,
891 rows.

Browser replay and observed results:

1. Open the cell's Filter menu. It uses 24px outlined controls, muted labels,
   full-width dividers and a neutral Add filter button.
1. Select `survived_label`, `equals`, and value `1`; press Enter.
   The menu closes, a filter chip appears and the table shows 342 matching rows.
   All ten displayed rows have survived_label 1.
1. Remove the filter. The table returns to 891 rows.
1. Add `survived_label is empty`. No value field is shown or required; clicking
   Add filter produces the chip and the expected 0-match empty state.
1. Remove the filter and reopen the menu. Escape dismisses it without adding
   a filter.

Screenshot: `/private/tmp/workshop-filter-menu.jpg` (local artifact).

Validation from `frontend/`, all passed:

```sh
bun run typecheck
bun run lint
bun run check:all
```

Logs: `/private/tmp/workshop-filter-style-{typecheck,lint,design}.log`.
Unit suites were not run for this presentation change.
