# Water-filling uniqueness

For any finite list of rational donor rows, every nonnegative allocation attaining the water level with the same total as the coordinate shortfalls equals the shortfall allocation in each row.

The water level is given. Its existence and continuity, and convergence under every fair schedule, remain in the manuscript.

[Lean source](Q132Water.lean) · [Mathematical source](../paper/manuscript.tex) · [Expected axiom report](expected-axioms.txt)

Replay from this directory with Lean 4.30.0 and its standard library.

```sh
lean -DwarningAsError=true Q132Water.lean > axioms.actual
diff -u expected-axioms.txt axioms.actual
```
