# Claims and evidence

| Claim | Status | Evidence |
|---|---|---|
| For finite Leontief donor coordination with positive budgets, nonempty supports and arbitrary nonnegative weights, the aggregate under best responses from zero converges to the unique Nash-welfare allocation for every fair schedule. | Proved, internally reviewed | [Manuscript](paper/manuscript.pdf) and [proof audit](audits/public_safe_reports/MATHEMATICAL_AUDIT.md) |
| On a specified three-donor instance, a floating-point replay checked potential monotonicity and agreement of aggregate allocations after 74 increasing-gap schedule blocks. | Computational corroboration | [Source](verification/src/replay.py) and [replay output](verification/logs/replay.txt) |
| Historical scope and attribution | Search through 26 November 2026 | [Literature review](audits/public_safe_reports/LITERATURE_AUDIT.md) |

## Partial Lean verification

For any finite list of rational donor rows, every nonnegative allocation attaining the water level with the same total as the coordinate shortfalls equals the shortfall allocation in each row. [Scope, source and replay](formalization/README.md)
